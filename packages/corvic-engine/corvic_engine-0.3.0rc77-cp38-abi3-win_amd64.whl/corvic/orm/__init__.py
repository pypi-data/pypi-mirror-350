"""Data model definitions; backed by an RDBMS."""

from __future__ import annotations

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm as sa_orm

from corvic.orm._proto_columns import ProtoMessageDecorator
from corvic.orm.base import Base, OrgBase
from corvic.orm.errors import (
    DeletedObjectError,
    InvalidORMIdentifierError,
    RequestedObjectsForNobodyError,
)
from corvic.orm.ids import (
    AgentID,
    AgentMessageID,
    BaseID,
    BaseIDFromInt,
    CompletionModelID,
    FeatureViewID,
    FeatureViewSourceID,
    IntIDDecorator,
    MessageEntryID,
    OrgID,
    PipelineID,
    ResourceID,
    RoomID,
    SourceID,
    SpaceID,
    SpaceParametersID,
    SpaceRunID,
    UserMessageID,
)
from corvic.orm.keys import (
    INT_PK_TYPE,
    ForeignKey,
    primary_key_foreign_column,
    primary_key_identity_column,
    primary_key_uuid_column,
)
from corvic.orm.mixins import (
    BelongsToOrgMixin,
    Session,
    SoftDeleteMixin,
    live_unique_constraint,
)
from corvic_generated.orm.v1 import (
    common_pb2,
    completion_model_pb2,
    feature_view_pb2,
    pipeline_pb2,
    space_pb2,
    table_pb2,
)
from corvic_generated.status.v1 import event_pb2

# NOTE: The only safe use of "sa_orm.relationship" uses the args:
# `viewonly=True` and `init=False`. Writes quickly become
# a complex mess when implementers of commit need to reason about
# which sub-object should be updated.
#
# Rather, classes in corvic.model define their own commit protocols,
# and if sub-orm-model updates are required they are explicit.


class Org(SoftDeleteMixin, OrgBase, kw_only=True):
    """An organization it a top level grouping of resources."""


class Room(BelongsToOrgMixin, SoftDeleteMixin, Base, kw_only=True):
    """A Room is a logical collection of Documents."""

    __tablename__ = "room"
    __table_args__ = (live_unique_constraint("name", "org_id"),)

    name: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text, default=None)
    id: sa_orm.Mapped[RoomID | None] = primary_key_identity_column()

    @property
    def room_key(self):
        return self.name


class BelongsToRoomMixin(sa_orm.MappedAsDataclass):
    room_id: sa_orm.Mapped[RoomID | None] = sa_orm.mapped_column(
        ForeignKey(Room).make(ondelete="CASCADE"),
        nullable=True,
        default=None,
    )


class DefaultObjects(Base, kw_only=True):
    """Holds the identifiers for default objects."""

    __tablename__ = "default_objects"
    default_org: sa_orm.Mapped[OrgID | None] = sa_orm.mapped_column(
        ForeignKey(Org).make(ondelete="CASCADE"),
        nullable=False,
    )
    default_room: sa_orm.Mapped[RoomID | None] = sa_orm.mapped_column(
        ForeignKey(Room).make(ondelete="CASCADE"), nullable=True, default=None
    )
    version: sa_orm.Mapped[int | None] = primary_key_identity_column(type_=INT_PK_TYPE)


class Resource(BelongsToOrgMixin, BelongsToRoomMixin, Base, kw_only=True):
    """A Resource is a reference to some durably stored file.

    E.g., a document could be a PDF file, an image, or a text transcript of a
    conversation
    """

    __tablename__ = "resource"

    name: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text)
    mime_type: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text)
    url: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text)
    md5: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.CHAR(32), nullable=True)
    size: sa_orm.Mapped[int] = sa_orm.mapped_column(nullable=True)
    original_path: sa_orm.Mapped[str] = sa_orm.mapped_column(nullable=True)
    description: sa_orm.Mapped[str] = sa_orm.mapped_column(nullable=True)
    id: sa_orm.Mapped[ResourceID | None] = primary_key_identity_column()
    latest_event: sa_orm.Mapped[event_pb2.Event | None] = sa_orm.mapped_column(
        default=None, nullable=True
    )
    is_terminal: sa_orm.Mapped[bool | None] = sa_orm.mapped_column(
        default=None, nullable=True
    )
    pipeline_ref: sa_orm.Mapped[PipelineInput | None] = sa_orm.relationship(
        init=False, viewonly=True
    )


class Source(BelongsToOrgMixin, BelongsToRoomMixin, Base, kw_only=True):
    """A source."""

    __tablename__ = "source"
    __table_args__ = (sa.UniqueConstraint("name", "room_id"),)

    name: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text)
    # protobuf describing the operations required to construct a table
    table_op_graph: sa_orm.Mapped[table_pb2.TableComputeOp] = sa_orm.mapped_column()
    id: sa_orm.Mapped[SourceID | None] = primary_key_identity_column()

    source_files: sa_orm.Mapped[common_pb2.BlobUrlList | None] = sa_orm.mapped_column(
        default=None
    )
    pipeline_ref: sa_orm.Mapped[PipelineOutput | None] = sa_orm.relationship(
        init=False, viewonly=True
    )

    @property
    def source_key(self):
        return self.name


class Pipeline(BelongsToOrgMixin, BelongsToRoomMixin, Base, kw_only=True):
    """A resource to source pipeline."""

    __tablename__ = "pipeline"
    __table_args__ = (sa.UniqueConstraint("name", "room_id"),)

    transformation: sa_orm.Mapped[pipeline_pb2.PipelineTransformation] = (
        sa_orm.mapped_column()
    )
    name: sa_orm.Mapped[str] = sa_orm.mapped_column()
    description: sa_orm.Mapped[str | None] = sa_orm.mapped_column()
    id: sa_orm.Mapped[PipelineID | None] = primary_key_identity_column()

    outputs: sa_orm.Mapped[list[PipelineOutput]] = sa_orm.relationship(
        viewonly=True,
        init=False,
        default_factory=list,
    )


class PipelineInput(BelongsToOrgMixin, BelongsToRoomMixin, Base, kw_only=True):
    """Pipeline input resources."""

    __tablename__ = "pipeline_input"
    __table_args__ = (sa.UniqueConstraint("name", "pipeline_id"),)

    resource: sa_orm.Mapped[Resource] = sa_orm.relationship(viewonly=True, init=False)
    name: sa_orm.Mapped[str]
    """A name the pipeline uses to refer to this input."""

    pipeline_id: sa_orm.Mapped[PipelineID] = primary_key_foreign_column(
        ForeignKey(Pipeline).make(ondelete="CASCADE")
    )
    resource_id: sa_orm.Mapped[ResourceID] = primary_key_foreign_column(
        ForeignKey(Resource).make(ondelete="CASCADE")
    )


class PipelineOutput(BelongsToOrgMixin, BelongsToRoomMixin, Base, kw_only=True):
    """Objects for tracking pipeline output sources."""

    __tablename__ = "pipeline_output"
    __table_args__ = (sa.UniqueConstraint("name", "pipeline_id"),)

    source: sa_orm.Mapped[Source] = sa_orm.relationship(viewonly=True, init=False)
    name: sa_orm.Mapped[str]
    """A name the pipeline uses to refer to this output."""

    pipeline_id: sa_orm.Mapped[PipelineID] = primary_key_foreign_column(
        ForeignKey(Pipeline).make(ondelete="CASCADE")
    )
    source_id: sa_orm.Mapped[SourceID] = primary_key_foreign_column(
        ForeignKey(Source).make(ondelete="CASCADE")
    )


class FeatureView(
    SoftDeleteMixin, BelongsToOrgMixin, BelongsToRoomMixin, Base, kw_only=True
):
    """A FeatureView is a logical collection of sources used by various spaces."""

    __tablename__ = "feature_view"
    __table_args__ = (live_unique_constraint("name", "room_id"),)

    id: sa_orm.Mapped[FeatureViewID | None] = primary_key_identity_column()
    name: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text, default=None)
    description: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text, default="")

    feature_view_output: sa_orm.Mapped[feature_view_pb2.FeatureViewOutput | None] = (
        sa_orm.mapped_column(default_factory=feature_view_pb2.FeatureViewOutput)
    )

    @property
    def feature_view_key(self):
        return self.name

    feature_view_sources: sa_orm.Mapped[list[FeatureViewSource]] = sa_orm.relationship(
        viewonly=True,
        init=False,
        default_factory=list,
    )


class FeatureViewSource(BelongsToOrgMixin, BelongsToRoomMixin, Base, kw_only=True):
    """A source inside of a feature view."""

    __tablename__ = "feature_view_source"

    table_op_graph: sa_orm.Mapped[table_pb2.TableComputeOp] = sa_orm.mapped_column()
    feature_view_id: sa_orm.Mapped[FeatureViewID] = sa_orm.mapped_column(
        ForeignKey(FeatureView).make(ondelete="CASCADE"),
        nullable=False,
    )
    id: sa_orm.Mapped[FeatureViewSourceID | None] = primary_key_identity_column()
    drop_disconnected: sa_orm.Mapped[bool] = sa_orm.mapped_column(default=False)
    # this should be legal but pyright complains that it makes Source depend
    # on itself
    source_id: sa_orm.Mapped[SourceID] = sa_orm.mapped_column(
        ForeignKey(Source).make(ondelete="CASCADE"),
        nullable=False,
        default=None,
    )
    source: sa_orm.Mapped[Source] = sa_orm.relationship(
        init=True, viewonly=True, default=None
    )


class Space(BelongsToOrgMixin, BelongsToRoomMixin, Base, kw_only=True):
    """A space is a named evaluation of space parameters."""

    __tablename__ = "space"
    __table_args__ = (sa.UniqueConstraint("name", "room_id"),)

    id: sa_orm.Mapped[SpaceID | None] = primary_key_identity_column()
    name: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text, default=None)
    description: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text, default="")

    feature_view_id: sa_orm.Mapped[FeatureViewID] = sa_orm.mapped_column(
        ForeignKey(FeatureView).make(ondelete="CASCADE"),
        nullable=False,
        default=None,
    )
    parameters: sa_orm.Mapped[space_pb2.SpaceParameters | None] = sa_orm.mapped_column(
        default=None
    )
    auto_sync: sa_orm.Mapped[bool | None] = sa_orm.mapped_column(default=None)
    feature_view: sa_orm.Mapped[FeatureView] = sa_orm.relationship(
        init=False,
        default=None,
        viewonly=True,
    )

    @property
    def space_key(self):
        return self.name


class CompletionModel(SoftDeleteMixin, BelongsToOrgMixin, Base, kw_only=True):
    """A customer's custom completion model definition."""

    __tablename__ = "completion_model"
    __table_args__ = (live_unique_constraint("name", "org_id"),)

    id: sa_orm.Mapped[CompletionModelID | None] = primary_key_identity_column()
    name: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text, default=None)
    description: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text, default=None)
    parameters: sa_orm.Mapped[completion_model_pb2.CompletionModelParameters | None] = (
        sa_orm.mapped_column(default=None)
    )
    secret_api_key: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text, default=None)
    last_validation_time: sa_orm.Mapped[datetime | None] = sa_orm.mapped_column(
        sa.DateTime(timezone=True),
        server_default=None,
        default=None,
    )
    last_successful_validation: sa_orm.Mapped[datetime | None] = sa_orm.mapped_column(
        sa.DateTime(timezone=True),
        server_default=None,
        default=None,
    )

    @property
    def model_key(self):
        return self.name


ID = (
    AgentID
    | AgentMessageID
    | CompletionModelID
    | FeatureViewID
    | FeatureViewSourceID
    | MessageEntryID
    | OrgID
    | PipelineID
    | ResourceID
    | RoomID
    | SourceID
    | SpaceID
    | SpaceParametersID
    | SpaceRunID
    | UserMessageID
)


__all__ = [
    "AgentID",
    "AgentMessageID",
    "Base",
    "BaseID",
    "BaseIDFromInt",
    "BelongsToOrgMixin",
    "CompletionModel",
    "CompletionModelID",
    "DefaultObjects",
    "DeletedObjectError",
    "FeatureView",
    "FeatureViewID",
    "FeatureViewSource",
    "FeatureViewSourceID",
    "ID",
    "InvalidORMIdentifierError",
    "MessageEntryID",
    "Org",
    "OrgID",
    "PipelineID",
    "PipelineInput",
    "PipelineOutput",
    "RequestedObjectsForNobodyError",
    "Resource",
    "ResourceID",
    "Room",
    "RoomID",
    "Session",
    "Source",
    "SourceID",
    "Space",
    "SpaceID",
    "SpaceParametersID",
    "SpaceRunID",
    "UserMessageID",
    "primary_key_foreign_column",
    "primary_key_identity_column",
    "primary_key_uuid_column",
    "ProtoMessageDecorator",
    "IntIDDecorator",
]
