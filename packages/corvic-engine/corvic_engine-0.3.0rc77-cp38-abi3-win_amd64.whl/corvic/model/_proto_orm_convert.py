import datetime
from collections.abc import Callable, Sequence
from typing import Any, Protocol, TypeVar

import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
from google.protobuf import timestamp_pb2

from corvic import orm
from corvic.result import InternalError, InvalidArgumentError, Ok
from corvic_generated.model.v1alpha import models_pb2
from corvic_generated.orm.v1 import feature_view_pb2

UNCOMMITTED_ID_PREFIX = "__uncommitted_object-"

ID = TypeVar("ID", bound=orm.BaseID[Any])


class _ModelProto(Protocol):
    id: str
    created_at: timestamp_pb2.Timestamp


class _ModelBelongsToOrgProto(_ModelProto, Protocol):
    org_id: str


class _ModelBelongsToRoomProto(_ModelBelongsToOrgProto, Protocol):
    room_id: str


ProtoObj = TypeVar("ProtoObj", bound=_ModelProto)
ProtoBelongsToOrgObj = TypeVar("ProtoBelongsToOrgObj", bound=_ModelBelongsToOrgProto)
ProtoBelongsToRoomObj = TypeVar("ProtoBelongsToRoomObj", bound=_ModelBelongsToRoomProto)


class _OrmModel(Protocol[ID]):
    id: sa_orm.Mapped[ID | None]

    @sa.ext.hybrid.hybrid_property
    def created_at(self) -> datetime.datetime | None: ...

    @created_at.inplace.expression
    @classmethod
    def _created_at_expression(cls): ...


class _OrmBelongsToOrgModel(_OrmModel[ID], Protocol):
    org_id: sa_orm.Mapped[orm.OrgID | None]


class _OrmBelongsToRoomModel(_OrmBelongsToOrgModel[ID], Protocol):
    room_id: sa_orm.Mapped[orm.RoomID | None]


OrmObj = TypeVar("OrmObj", bound=_OrmModel[Any])
OrmBelongsToOrgObj = TypeVar("OrmBelongsToOrgObj", bound=_OrmBelongsToOrgModel[Any])
OrmBelongsToRoomObj = TypeVar("OrmBelongsToRoomObj", bound=_OrmBelongsToRoomModel[Any])


def _orm_id_to_str(id: orm.ID | None):
    if id:
        return str(id)
    return ""


def _translate_orm_id(
    obj_id: str, id_class: type[ID]
) -> Ok[ID | None] | orm.InvalidORMIdentifierError:
    if obj_id.startswith(UNCOMMITTED_ID_PREFIX):
        return Ok(None)
    parsed_obj_id = id_class(obj_id)
    match parsed_obj_id.to_db():
        case orm.InvalidORMIdentifierError() as err:
            return err
        case Ok():
            return Ok(parsed_obj_id)


def timestamp_orm_to_proto(
    timestamp_orm: datetime.datetime | None,
) -> timestamp_pb2.Timestamp | None:
    if timestamp_orm is not None:
        timestamp_proto = timestamp_pb2.Timestamp()
        timestamp_proto.FromDatetime(timestamp_orm)
    else:
        timestamp_proto = None
    return timestamp_proto


def resource_orm_to_proto(resource_orm: orm.Resource) -> models_pb2.Resource:
    pipeline_input_name = ""
    pipeline_id = ""
    if resource_orm.pipeline_ref:
        pipeline_input_name = resource_orm.pipeline_ref.name
        pipeline_id = _orm_id_to_str(resource_orm.pipeline_ref.pipeline_id)
    return models_pb2.Resource(
        id=_orm_id_to_str(resource_orm.id),
        name=resource_orm.name,
        description=resource_orm.description,
        mime_type=resource_orm.mime_type,
        url=resource_orm.url,
        md5=resource_orm.md5,
        size=resource_orm.size,
        original_path=resource_orm.original_path,
        room_id=_orm_id_to_str(resource_orm.room_id),
        org_id=_orm_id_to_str(resource_orm.org_id),
        recent_events=[resource_orm.latest_event] if resource_orm.latest_event else [],
        is_terminal=bool(resource_orm.is_terminal),
        pipeline_id=pipeline_id,
        pipeline_input_name=pipeline_input_name,
        created_at=timestamp_orm_to_proto(resource_orm.created_at),
    )


def source_orm_to_proto(source_orm: orm.Source) -> models_pb2.Source:
    return models_pb2.Source(
        id=_orm_id_to_str(source_orm.id),
        name=source_orm.name,
        table_op_graph=source_orm.table_op_graph,
        room_id=_orm_id_to_str(source_orm.room_id),
        org_id=_orm_id_to_str(source_orm.org_id),
        pipeline_id=_orm_id_to_str(source_orm.pipeline_ref.pipeline_id)
        if source_orm.pipeline_ref
        else "",
        created_at=timestamp_orm_to_proto(source_orm.created_at),
    )


def feature_view_source_orm_to_proto(
    feature_view_source_orm: orm.FeatureViewSource,
) -> models_pb2.FeatureViewSource:
    if feature_view_source_orm.table_op_graph.WhichOneof("op") is not None:
        op = feature_view_source_orm.table_op_graph
    else:
        # some legacy feature views were stored without op graphs fill those
        # with the source's opgraph
        op = feature_view_source_orm.source.table_op_graph
    return models_pb2.FeatureViewSource(
        id=_orm_id_to_str(feature_view_source_orm.id),
        room_id=_orm_id_to_str(feature_view_source_orm.room_id),
        source=source_orm_to_proto(feature_view_source_orm.source),
        table_op_graph=op,
        drop_disconnected=feature_view_source_orm.drop_disconnected,
        org_id=_orm_id_to_str(feature_view_source_orm.org_id),
        created_at=timestamp_orm_to_proto(feature_view_source_orm.created_at),
    )


def feature_view_orm_to_proto(
    feature_view_orm: orm.FeatureView,
) -> models_pb2.FeatureView:
    return models_pb2.FeatureView(
        id=_orm_id_to_str(feature_view_orm.id),
        name=feature_view_orm.name,
        description=feature_view_orm.description,
        room_id=_orm_id_to_str(feature_view_orm.room_id),
        feature_view_output=feature_view_orm.feature_view_output,
        feature_view_sources=[
            feature_view_source_orm_to_proto(fvs)
            for fvs in feature_view_orm.feature_view_sources
        ],
        org_id=_orm_id_to_str(feature_view_orm.org_id),
        created_at=timestamp_orm_to_proto(feature_view_orm.created_at),
    )


def pipeline_orm_to_proto(
    pipeline_orm: orm.Pipeline,
) -> models_pb2.Pipeline:
    return models_pb2.Pipeline(
        id=_orm_id_to_str(pipeline_orm.id),
        name=pipeline_orm.name,
        room_id=_orm_id_to_str(pipeline_orm.room_id),
        source_outputs={
            output_obj.name: source_orm_to_proto(output_obj.source)
            for output_obj in pipeline_orm.outputs
        },
        pipeline_transformation=pipeline_orm.transformation,
        org_id=_orm_id_to_str(pipeline_orm.org_id),
        description=pipeline_orm.description,
        created_at=timestamp_orm_to_proto(pipeline_orm.created_at),
    )


def space_orm_to_proto(space_orm: orm.Space) -> models_pb2.Space:
    return models_pb2.Space(
        id=_orm_id_to_str(space_orm.id),
        name=space_orm.name,
        description=space_orm.description,
        room_id=_orm_id_to_str(space_orm.room_id),
        space_parameters=space_orm.parameters,
        feature_view=feature_view_orm_to_proto(space_orm.feature_view),
        auto_sync=space_orm.auto_sync if space_orm.auto_sync is not None else False,
        org_id=_orm_id_to_str(space_orm.org_id),
        created_at=timestamp_orm_to_proto(space_orm.created_at),
    )


def room_orm_to_proto(room_orm: orm.Room) -> models_pb2.Room:
    return models_pb2.Room(
        id=_orm_id_to_str(room_orm.id),
        name=room_orm.name,
        org_id=_orm_id_to_str(room_orm.org_id),
        created_at=timestamp_orm_to_proto(room_orm.created_at),
    )


def completion_model_orm_to_proto(
    completion_model_orm: orm.CompletionModel,
) -> models_pb2.CompletionModel:
    return models_pb2.CompletionModel(
        id=_orm_id_to_str(completion_model_orm.id),
        name=completion_model_orm.name,
        description=completion_model_orm.description,
        org_id=_orm_id_to_str(completion_model_orm.org_id),
        parameters=completion_model_orm.parameters,
        secret_api_key=completion_model_orm.secret_api_key,
        created_at=timestamp_orm_to_proto(completion_model_orm.created_at),
        last_validation_time=timestamp_orm_to_proto(
            completion_model_orm.last_validation_time
        ),
        last_successful_validation=timestamp_orm_to_proto(
            completion_model_orm.last_successful_validation
        ),
    )


def add_orm_org_mixin_to_session(
    orm_obj: OrmBelongsToOrgObj,
    proto_obj: _ModelBelongsToOrgProto,
    id_class: type[ID],
    session: sa_orm.Session,
) -> Ok[OrmBelongsToOrgObj] | orm.InvalidORMIdentifierError:
    match _translate_orm_id(proto_obj.id, id_class):
        case Ok(orm_id):
            orm_obj.id = orm_id
        case orm.InvalidORMIdentifierError() as err:
            return err
    if proto_obj.org_id:
        org_id = orm.OrgID(proto_obj.org_id)
        match org_id.to_db():
            case Ok():
                orm_obj.org_id = org_id
            case orm.InvalidORMIdentifierError() as err:
                return err
        orm_obj.org_id = org_id
    if not orm_obj.id:
        session.add(orm_obj)
    else:
        orm_obj = session.merge(orm_obj)
    return Ok(orm_obj)


def add_orm_room_mixin_to_session(
    orm_obj: OrmBelongsToRoomObj,
    proto_obj: _ModelBelongsToRoomProto,
    id_class: type[ID],
    session: sa_orm.Session,
) -> Ok[OrmBelongsToRoomObj] | orm.InvalidORMIdentifierError:
    room_id = orm.RoomID(proto_obj.room_id)
    match room_id.to_db():
        case Ok():
            pass
        case orm.InvalidORMIdentifierError() as err:
            return err
    orm_obj.room_id = orm.RoomID(proto_obj.room_id)
    return add_orm_org_mixin_to_session(orm_obj, proto_obj, id_class, session)


def _resource_pipeline_to_orm(
    proto_obj: models_pb2.Resource, orm_obj: orm.Resource, session: sa_orm.Session
) -> Ok[None] | InvalidArgumentError:
    if proto_obj.pipeline_id:
        match _translate_orm_id(proto_obj.pipeline_id, orm.PipelineID):
            case orm.InvalidORMIdentifierError() as err:
                return err
            case Ok(pipeline_id):
                pass
        if not pipeline_id:
            return InvalidArgumentError("resource's pipeline cannot be anonymous")
        session.flush()
        if not orm_obj.id:
            raise InternalError("internal assertion did not hold")
        pipeline_input = orm.PipelineInput(
            resource_id=orm_obj.id,
            name=proto_obj.pipeline_input_name,
            pipeline_id=pipeline_id,
            room_id=orm_obj.room_id,
        )
        if orm_obj.org_id:
            pipeline_input.org_id = orm_obj.org_id
        orm_obj.pipeline_ref = session.merge(pipeline_input)
    return Ok(None)


def resource_proto_to_orm(
    proto_obj: models_pb2.Resource, session: sa_orm.Session
) -> Ok[orm.Resource] | InvalidArgumentError:
    orm_obj = orm.Resource(
        name=proto_obj.name,
        description=proto_obj.description,
        mime_type=proto_obj.mime_type,
        md5=proto_obj.md5,
        url=proto_obj.url,
        size=proto_obj.size,
        original_path=proto_obj.original_path,
        latest_event=proto_obj.recent_events[-1] if proto_obj.recent_events else None,
        is_terminal=proto_obj.is_terminal,
    )
    add_orm_room_mixin_to_session(orm_obj, proto_obj, orm.ResourceID, session)

    match _resource_pipeline_to_orm(proto_obj, orm_obj, session):
        case Ok(None):
            return Ok(orm_obj)
        case InvalidArgumentError() as err:
            return err


def _ensure_id(
    proto_obj: ProtoObj,
    proto_to_orm: Callable[
        [ProtoObj, sa_orm.Session], Ok[OrmObj] | InvalidArgumentError
    ],
    id_type: type[ID],
    session: sa_orm.Session,
) -> Ok[ID] | orm.InvalidORMIdentifierError | InvalidArgumentError:
    match _translate_orm_id(proto_obj.id, id_type):
        case orm.InvalidORMIdentifierError() as err:
            return err
        case Ok(orm_id):
            if orm_id:
                return Ok(orm_id)
    match proto_to_orm(proto_obj, session):
        case orm.InvalidORMIdentifierError() | InvalidArgumentError() as err:
            return err
        case Ok(orm_obj):
            session.flush()
            if not orm_obj.id:
                raise InternalError("internal assertion did not hold")
            return Ok(orm_obj.id)


def pipeline_proto_to_orm(  # noqa: C901
    proto_obj: models_pb2.Pipeline, session: sa_orm.Session
) -> Ok[orm.Pipeline] | orm.InvalidORMIdentifierError | InvalidArgumentError:
    orm_obj = orm.Pipeline(
        name=proto_obj.name,
        transformation=proto_obj.pipeline_transformation,
        description=proto_obj.description,
    )
    if proto_obj.org_id:
        orm_obj.org_id = orm.OrgID(proto_obj.org_id)
    match add_orm_room_mixin_to_session(orm_obj, proto_obj, orm.PipelineID, session):
        case Ok(orm_obj):
            pass
        case orm.InvalidORMIdentifierError() as err:
            return err
    session.flush()

    if not orm_obj.id:
        raise InternalError("internal assertion did not hold")

    outputs = list[orm.PipelineOutput]()
    for name, val in proto_obj.source_outputs.items():
        match _ensure_id(val, source_proto_to_orm, orm.SourceID, session):
            case orm.InvalidORMIdentifierError() | InvalidArgumentError() as err:
                return err
            case Ok(source_id):
                pass
        outputs.append(
            orm.PipelineOutput(
                source_id=source_id,
                name=name,
                pipeline_id=orm_obj.id,
                room_id=orm_obj.room_id,
            )
        )

    if proto_obj.org_id:
        org_id = orm.OrgID(proto_obj.org_id)
        for obj in outputs:
            obj.org_id = org_id
    for obj in outputs:
        session.merge(obj)
    return Ok(orm_obj)


def source_proto_to_orm(
    proto_obj: models_pb2.Source, session: sa_orm.Session
) -> Ok[orm.Source] | orm.InvalidORMIdentifierError | InvalidArgumentError:
    orm_obj = orm.Source(
        name=proto_obj.name,
        table_op_graph=proto_obj.table_op_graph,
    )
    return add_orm_room_mixin_to_session(orm_obj, proto_obj, orm.SourceID, session)


def space_proto_to_orm(
    proto_obj: models_pb2.Space, session: sa_orm.Session
) -> Ok[orm.Space] | orm.InvalidORMIdentifierError | InvalidArgumentError:
    match _ensure_id(
        proto_obj.feature_view, feature_view_proto_to_orm, orm.FeatureViewID, session
    ):
        case orm.InvalidORMIdentifierError() | InvalidArgumentError() as err:
            return err
        case Ok(feature_view_id):
            pass

    if not feature_view_id:
        raise InternalError("internal assertion did not hold")

    orm_obj = orm.Space(
        name=proto_obj.name,
        description=proto_obj.description,
        feature_view_id=feature_view_id,
        parameters=proto_obj.space_parameters,
        auto_sync=proto_obj.auto_sync,
    )
    return add_orm_room_mixin_to_session(orm_obj, proto_obj, orm.SpaceID, session)


def feature_view_proto_to_orm(
    proto_obj: models_pb2.FeatureView, session: sa_orm.Session
) -> Ok[orm.FeatureView] | orm.InvalidORMIdentifierError | InvalidArgumentError:
    orm_obj = orm.FeatureView(
        name=proto_obj.name,
        description=proto_obj.description,
    )
    if proto_obj.org_id:
        orm_obj.org_id = orm.OrgID(proto_obj.org_id)
    match add_orm_room_mixin_to_session(orm_obj, proto_obj, orm.FeatureViewID, session):
        case Ok(orm_obj):
            pass
        case orm.InvalidORMIdentifierError() as err:
            return err
    session.flush()

    if not orm_obj.id or not orm_obj.room_id:
        raise InternalError("internal assertion did not hold")

    new_fv_sources = list[orm.FeatureViewSource]()
    for fvs in proto_obj.feature_view_sources:
        match _feature_view_source_proto_to_orm(
            fvs, orm_obj.room_id, orm_obj.id, session
        ):
            case orm.InvalidORMIdentifierError() | InvalidArgumentError() as err:
                return err
            case Ok(fvs_orm):
                new_fv_sources.append(fvs_orm)

    old_to_new_source_id = dict[str, str]()
    for old_fvs, new_fvs in zip(
        proto_obj.feature_view_sources, new_fv_sources, strict=True
    ):
        if old_fvs.source.id != str(new_fvs.source_id):
            old_to_new_source_id[old_fvs.source.id] = str(new_fvs.source_id)

    orm_obj.feature_view_output = (
        feature_view_pb2.FeatureViewOutput(
            relationships=[
                feature_view_pb2.FeatureViewRelationship(
                    start_source_id=old_to_new_source_id.get(
                        old_rel.start_source_id, old_rel.start_source_id
                    ),
                    end_source_id=old_to_new_source_id.get(
                        old_rel.end_source_id, old_rel.end_source_id
                    ),
                )
                for old_rel in proto_obj.feature_view_output.relationships
            ],
            output_sources=[
                feature_view_pb2.OutputSource(
                    source_id=old_to_new_source_id.get(
                        old_output_source.source_id, old_output_source.source_id
                    )
                )
                for old_output_source in proto_obj.feature_view_output.output_sources
            ],
        )
        if old_to_new_source_id
        else proto_obj.feature_view_output
    )
    orm_obj = session.merge(orm_obj)
    return Ok(orm_obj)


def _feature_view_source_proto_to_orm(
    proto_obj: models_pb2.FeatureViewSource,
    room_id: orm.RoomID,
    feature_view_id: orm.FeatureViewID,
    session: sa_orm.Session,
) -> Ok[orm.FeatureViewSource] | orm.InvalidORMIdentifierError | InvalidArgumentError:
    match _ensure_id(proto_obj.source, source_proto_to_orm, orm.SourceID, session):
        case orm.InvalidORMIdentifierError() | InvalidArgumentError() as err:
            return err
        case Ok(source_id):
            pass

    proto_obj.room_id = proto_obj.room_id or str(room_id)
    orm_obj = orm.FeatureViewSource(
        table_op_graph=proto_obj.table_op_graph,
        drop_disconnected=proto_obj.drop_disconnected,
        source_id=source_id,
        feature_view_id=feature_view_id,
    )
    return add_orm_room_mixin_to_session(
        orm_obj, proto_obj, orm.FeatureViewSourceID, session
    )


def room_proto_to_orm(
    proto_obj: models_pb2.Room, session: sa_orm.Session
) -> Ok[orm.Room] | orm.InvalidORMIdentifierError | InvalidArgumentError:
    orm_obj = orm.Room(name=proto_obj.name)
    return add_orm_org_mixin_to_session(orm_obj, proto_obj, orm.RoomID, session)


def completion_model_proto_to_orm(
    proto_obj: models_pb2.CompletionModel, session: sa_orm.Session
) -> Ok[orm.CompletionModel] | InvalidArgumentError:
    orm_obj = orm.CompletionModel(
        name=proto_obj.name,
        description=proto_obj.description,
        parameters=proto_obj.parameters,
        secret_api_key=proto_obj.secret_api_key,
        last_validation_time=proto_obj.last_validation_time.ToDatetime(),
        last_successful_validation=proto_obj.last_successful_validation.ToDatetime(),
    )
    return add_orm_org_mixin_to_session(
        orm_obj, proto_obj, orm.CompletionModelID, session
    )


def source_delete_orms(
    orm_ids: Sequence[orm.SourceID],
    session: sa_orm.Session,
) -> Ok[None] | InvalidArgumentError:
    feat_view_refs = list(
        session.scalars(
            sa.select(orm.FeatureViewSource.id)
            .where(orm.FeatureViewSource.source_id.in_(orm_ids))
            .limit(1)
        )
    )

    if feat_view_refs:
        return InvalidArgumentError(
            "cannot delete a source that still has feature views"
        )
    session.execute(sa.delete(orm.Source).where(orm.Source.id.in_(orm_ids)))
    return Ok(None)


def pipeline_delete_orms(
    ids: Sequence[orm.PipelineID], session: sa_orm.Session
) -> Ok[None] | InvalidArgumentError:
    source_ids = [
        val[0]
        for val in session.execute(
            sa.select(orm.Source.id).where(
                orm.Source.id.in_(
                    sa.select(orm.PipelineOutput.source_id).where(
                        orm.PipelineOutput.pipeline_id.in_(ids)
                    )
                )
            )
        )
        if val[0] is not None
    ]
    match source_delete_orms(source_ids, session):
        case InvalidArgumentError() as err:
            return err
        case Ok():
            pass

    session.execute(
        sa.delete(orm.Resource).where(
            orm.Resource.id.in_(
                sa.select(orm.PipelineInput.resource_id)
                .join(orm.Pipeline)
                .where(orm.Pipeline.id.in_(ids))
            )
        )
    )
    session.execute(sa.delete(orm.Pipeline).where(orm.Pipeline.id.in_(ids)))
    return Ok(None)


def resource_delete_orms(
    ids: Sequence[orm.ResourceID],
    session: orm.Session,
) -> Ok[None] | InvalidArgumentError:
    pipeline_refs = list(
        session.execute(
            sa.select(orm.PipelineInput.pipeline_id)
            .where(orm.PipelineInput.resource_id.in_(ids))
            .limit(1)
        )
    )

    if pipeline_refs:
        return InvalidArgumentError(
            "sources exist that reference resources to be deleted"
        )
    session.execute(sa.delete(orm.Resource).where(orm.Resource.id.in_(ids)))
    return Ok(None)


def feature_view_source_delete_orms(
    ids: Sequence[orm.FeatureViewSourceID], session: orm.Session
) -> Ok[None] | InvalidArgumentError:
    feat_view_refs = list(
        session.execute(
            sa.select(orm.FeatureView.id)
            .where(
                orm.FeatureView.id.in_(
                    sa.select(orm.FeatureViewSource.feature_view_id).where(
                        orm.FeatureViewSource.id.in_(ids)
                    )
                )
            )
            .limit(1)
        )
    )
    if feat_view_refs:
        return InvalidArgumentError(
            "feature views exist that reference feature_view_sources to be deleted"
        )

    session.execute(
        sa.delete(orm.FeatureViewSource).where(orm.FeatureViewSource.id.in_(ids))
    )
    return Ok(None)


def feature_view_delete_orms(
    ids: Sequence[orm.FeatureViewID], session: orm.Session
) -> Ok[None] | InvalidArgumentError:
    space_refs = list(
        session.execute(
            sa.select(orm.Space.id).where(orm.Space.feature_view_id.in_(ids))
        )
    )
    if space_refs:
        return InvalidArgumentError(
            "spaces exist that reference feature_views to be deleted"
        )
    session.execute(sa.delete(orm.FeatureView).where(orm.FeatureView.id.in_(ids)))
    return Ok(None)


def space_delete_orms(
    ids: Sequence[orm.SpaceID], session: orm.Session
) -> Ok[None] | InvalidArgumentError:
    session.execute(sa.delete(orm.Space).where(orm.Space.id.in_(ids)))
    return Ok(None)


def room_delete_orms(
    ids: Sequence[orm.RoomID], session: orm.Session
) -> Ok[None] | InvalidArgumentError:
    source_refs = list(
        session.scalars(
            sa.select(orm.Source).where(orm.Source.room_id.in_(ids)).limit(1)
        )
    )
    if source_refs:
        return InvalidArgumentError("cannot delete a room that still has sources")

    session.execute(sa.delete(orm.Room).where(orm.Room.id.in_(ids)))
    return Ok(None)


def completion_model_delete_orms(
    ids: Sequence[orm.CompletionModelID],
    session: orm.Session,
) -> Ok[None] | InvalidArgumentError:
    session.execute(
        sa.delete(orm.CompletionModel).where(orm.CompletionModel.id.in_(ids))
    )
    return Ok(None)
