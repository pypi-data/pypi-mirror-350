"""Sources."""

from __future__ import annotations

import copy
import datetime
import functools
from collections.abc import Iterable, Mapping, Sequence
from typing import Self, TypeAlias

import polars as pl
import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
from sqlalchemy.orm.interfaces import LoaderOption

from corvic import op_graph, orm, system
from corvic.model._base_model import BelongsToRoomModel
from corvic.model._defaults import Defaults
from corvic.model._proto_orm_convert import (
    source_delete_orms,
    source_orm_to_proto,
    source_proto_to_orm,
)
from corvic.model._resource import Resource, ResourceID
from corvic.result import InvalidArgumentError, NotFoundError, Ok
from corvic.table import Table
from corvic_generated.model.v1alpha import models_pb2

SourceID: TypeAlias = orm.SourceID
RoomID: TypeAlias = orm.RoomID
PipelineID: TypeAlias = orm.PipelineID


def foreign_key(
    referenced_source: SourceID | Source, *, is_excluded: bool = False
) -> op_graph.feature_type.ForeignKey:
    match referenced_source:
        case SourceID():
            return op_graph.feature_type.foreign_key(
                referenced_source, is_excluded=is_excluded
            )
        case Source():
            return op_graph.feature_type.foreign_key(
                referenced_source.id, is_excluded=is_excluded
            )


class Source(BelongsToRoomModel[SourceID, models_pb2.Source, orm.Source]):
    """Sources describe how resources should be treated.

    Example:
    >>> Source.from_polars(order_data)
    >>>    .as_dimension_table()
    >>> )
    """

    @classmethod
    def orm_class(cls):
        return orm.Source

    @classmethod
    def id_class(cls):
        return SourceID

    @classmethod
    def orm_to_proto(cls, orm_obj: orm.Source) -> models_pb2.Source:
        return source_orm_to_proto(orm_obj)

    @classmethod
    def proto_to_orm(
        cls, proto_obj: models_pb2.Source, session: orm.Session
    ) -> Ok[orm.Source] | InvalidArgumentError:
        return source_proto_to_orm(proto_obj, session)

    @classmethod
    def delete_by_ids(
        cls, ids: Sequence[SourceID], session: orm.Session
    ) -> Ok[None] | InvalidArgumentError:
        return source_delete_orms(ids, session)

    @classmethod
    def from_id(
        cls,
        source_id: SourceID,
        client: system.Client | None = None,
        session: sa_orm.Session | None = None,
    ) -> Ok[Self] | NotFoundError:
        client = client or Defaults.get_default_client()
        return cls.load_proto_for(source_id, client, session).map(
            lambda proto_self: cls(client, proto_self)
        )

    @classmethod
    def from_proto(
        cls, proto: models_pb2.Source, client: system.Client | None = None
    ) -> Source:
        client = client or Defaults.get_default_client()
        return cls(client, proto)

    @classmethod
    def create(
        cls,
        name: str,
        client: system.Client | None = None,
        room_id: RoomID | None = None,
    ) -> Ok[Self] | InvalidArgumentError:
        """Create a new source to be populated later."""
        client = client or Defaults.get_default_client()
        room_id = room_id or Defaults.get_default_room_id(client)

        proto_source = models_pb2.Source(
            name=name,
            room_id=str(room_id),
        )

        return Ok(cls(client, proto_source))

    @classmethod
    def from_resource(
        cls,
        resource: Resource,
        name: str | None = None,
        client: system.Client | None = None,
        room_id: RoomID | None = None,
    ) -> Ok[Self] | system.DataMisplacedError | InvalidArgumentError:
        return cls.from_non_tabular_resource(resource, name, client, room_id).and_then(
            lambda new_source: Table.from_parquet_file(
                new_source.client, resource.url
            ).map(lambda table: new_source.with_table(table))
        )

    @classmethod
    def from_non_tabular_resource(
        cls,
        resource: Resource,
        name: str | None = None,
        client: system.Client | None = None,
        room_id: RoomID | None = None,
    ) -> Ok[Self] | InvalidArgumentError:
        """Construct a source for a resource that requires some preprocessing.

        This flavor populates all of the metadata that comes from the resource
        but does not populate table. Callers are expected to populate table later.
        """
        client = client or resource.client
        room_id = room_id or resource.room_id

        proto_source = models_pb2.Source(
            name=name or resource.name,
            room_id=str(room_id),
        )

        return Ok(cls(client, proto_source))

    @classmethod
    def from_polars(
        cls,
        name: str,
        data_frame: pl.DataFrame,
        client: system.Client | None = None,
        room_id: RoomID | None = None,
    ) -> Self:
        """Create a source from a pl.DataFrame.

        Args:
            name: a unique name for this source
            data_frame: a polars DataFrame
            client: use a particular system.Client instead of the default
            room_id: room to associate this source with. Use the default room if None.
        """
        client = client or Defaults.get_default_client()
        resource = (
            Resource.from_polars(data_frame, client, room_id=room_id)
            .commit()
            .unwrap_or_raise()
        )
        return cls.from_resource(
            resource, name=name, client=client, room_id=room_id
        ).unwrap_or_raise()

    def with_table(self, table: Table) -> Self:
        proto_self = copy.deepcopy(self.proto_self)
        proto_self.table_op_graph.CopyFrom(table.op_graph.to_proto())
        return self.__class__(
            self.client,
            proto_self=proto_self,
        )

    def with_property_table(self, props: Table) -> Self:
        proto_self = copy.deepcopy(self.proto_self)
        proto_self.prop_table_op_graph.CopyFrom(props.op_graph.to_proto())
        return self.__class__(
            self.client,
            proto_self=proto_self,
        )

    @classmethod
    def orm_load_options(cls) -> list[LoaderOption]:
        return [
            sa_orm.selectinload(orm.Source.pipeline_ref).selectinload(
                orm.PipelineOutput.source
            ),
        ]

    @classmethod
    def list(
        cls,
        *,
        room_id: RoomID | None = None,
        limit: int | None = None,
        resource_id: ResourceID | None = None,
        created_before: datetime.datetime | None = None,
        client: system.Client | None = None,
        ids: Iterable[SourceID] | None = None,
        existing_session: sa_orm.Session | None = None,
    ) -> Ok[list[Source]] | NotFoundError | InvalidArgumentError:
        """List sources that exist in storage."""
        client = client or Defaults.get_default_client()
        additional_query_transform = None

        if resource_id is not None:
            match Resource.from_id(resource_id, client):
                case NotFoundError():
                    return NotFoundError("resource not found", resource_id=resource_id)
                case Ok(resource):

                    def resource_filter(query: sa.Select[tuple[orm.Source]]):
                        return query.where(
                            orm.Source.id.in_(
                                sa.select(orm.PipelineOutput.source_id)
                                .join(orm.Pipeline)
                                .join(orm.PipelineInput)
                                .where(orm.PipelineInput.resource_id == resource.id)
                            )
                        )

                    additional_query_transform = resource_filter

        match cls.list_as_proto(
            client,
            limit=limit,
            room_id=room_id,
            created_before=created_before,
            ids=ids,
            additional_query_transform=additional_query_transform,
            existing_session=existing_session,
        ):
            case NotFoundError() | InvalidArgumentError() as err:
                return err
            case Ok(protos):
                return Ok([cls.from_proto(proto, client) for proto in protos])

    def with_feature_types(
        self, feature_types: Mapping[str, op_graph.FeatureType]
    ) -> Self:
        """Assign a Feature Type to each column in source.

        Args:
            feature_types: Mapping between column name and feature type

        Example:
        >>> with_feature_types(
        >>>        {
        >>>            "id": corvic.model.feature_type.primary_key(),
        >>>            "customer_id": corvic.model.feature_type.foreign_key(
        >>>                customer_source.id
        >>>            ),
        >>>        },
        >>>    )
        """
        return self.with_table(self.table.update_feature_types(feature_types))

    @functools.cached_property
    def table(self):
        return Table.from_ops(
            self.client, op_graph.op.from_proto(self.proto_self.table_op_graph)
        )

    @functools.cached_property
    def prop_table(self):
        return Table.from_ops(
            self.client, op_graph.op.from_proto(self.proto_self.prop_table_op_graph)
        )

    @property
    def name(self) -> str:
        return self.proto_self.name

    @property
    def pipeline_id(self) -> PipelineID | None:
        return PipelineID(self.proto_self.pipeline_id) or None
