import datetime
import strawberry
from typing import List, Optional, Union, Annotated
import typing
from uuid import UUID
import uuid


from sqlalchemy.util import typing
from GraphTypeDefinitions.BaseGQLModel import BaseGQLModel
from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo
from._GraphPermissions import OnlyForAuthentized

from GraphTypeDefinitions._GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_valid,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    resolve_rbacobject,
    createRootResolver_by_id,
    createRootResolver_by_page,
)

from GraphTypeDefinitions.workflowStateGQLModel import (
    WorkflowStateResultGQLModel,
    
)

UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]
GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".externals")]

WorkflowGQLModel = Annotated["WorkflowGQLModel", strawberry.lazy(".workflowGQLModel")]
WorkflowStateGQLModel = Annotated[
    "WorkflowStateGQLModel", strawberry.lazy(".workflowStateGQLModel")
]
# WorkflowStateResultGQLModel = Annotated[
#     "WorkflowStateResultGQLModel", strawberry.lazy(".workflowStateGQLModel")
# ]


@strawberry.federation.type(
    keys=["id"],
    description="""Entity defining users with some rights for the state in dataflow (node in graph)""",
)
class WorkflowStateUserGQLModel(BaseGQLModel):
    # @classmethod
    # async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
    #     loader = getLoaders(info).workflowstateusers
    #     result = await loader.load(id)
    #     if result is not None:
    #         result._type_definition = cls._type_definition  # little hack :)

    #         # some version of strawberry changed :(
    #     return result
    
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).workflowstateusers

    id = resolve_id
    valid = resolve_valid
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby
    rbacobject = resolve_rbacobject


    @strawberry.field(description="""User""", permission_classes=[OnlyForAuthentized()])
    def user(self) -> Optional[UserGQLModel]:
        from .externals import UserGQLModel

        return UserGQLModel(id=self.user_id)

    @strawberry.field(description="""Group for which the user has some right""", permission_classes=[OnlyForAuthentized()])
    def group(self) -> Optional[GroupGQLModel]:
        from .externals import GroupGQLModel

        return GroupGQLModel(id=self.group_id)

    @strawberry.field(description="""State""", permission_classes=[OnlyForAuthentized()])
    async def state(
        self, info: strawberry.types.Info
    ) -> Optional[WorkflowStateGQLModel]:
        loader = getLoadersFromInfo(info).workflowstates
        result = await loader.load(self.workflowstate_id)
        return result


#####################################################################
#
# Special fields for query
#
#####################################################################

from dataclasses import dataclass
from uoishelpers.resolvers import createInputs


@createInputs
@dataclass
class WorkflowStateUserWhereFilter:
    workflowstate_id: typing.Optional[uuid.UUID]
    user_id: typing.Optional[uuid.UUID]
    group_id: typing.Optional[uuid.UUID]

    from .workflowStateGQLModel import WorkflowStateWhereFilter
    
    states: WorkflowStateWhereFilter


workflow_state_user = createRootResolver_by_page(
    scalarType=WorkflowStateUserGQLModel,
    whereFilterType=WorkflowStateUserWhereFilter,
    description="""Returns users of workflow states by page""",
    loaderLambda=lambda info: getLoadersFromInfo(info).workflowstateusers,
)


workflow_state_user_by_id = createRootResolver_by_id(
    WorkflowStateUserGQLModel, description="""Returns workflow state user by ID"""
)


#####################################################################
#
# Mutation section
#
#####################################################################


@strawberry.input(description="""Input structure - C and U operation""")
class WorkflowStateAddUserGQLModel:
    workflowstate_id: UUID = strawberry.field(
        default=None, description="Identification of workflow state"
    )
    user_id: UUID = strawberry.field(default=None, description="Identification of user")
    group_id: UUID = strawberry.field(
        default=None,
        description="Identification of group for which the user has appropriate access level",
    )
    accesslevel: int = strawberry.field(description="access level")


@strawberry.input(description="""D operation""")
class WorkflowStateRemoveUserGQLModel:
    workflowstate_id: UUID = strawberry.field(
        default=None, description="Identification of workflow state"
    )
    user_id: UUID = strawberry.field(default=None, description="Identification of user")
    group_id: UUID = strawberry.field(
        default=None,
        description="Identification of group for which the user has appropriate access level",
    )


@strawberry.mutation(
    description="""Adds or updates a user & group at the workflow state""", permission_classes=[OnlyForAuthentized()]
)
async def workflow_state_add_user(
    self, info: strawberry.types.Info, payload: WorkflowStateAddUserGQLModel
) -> Optional["WorkflowStateResultGQLModel"]:
    
    loader = getLoadersFromInfo(info).workflowstateusers
    
    existing = await loader.filter_by(
        workflowstate_id=payload.workflowstate_id,
        user_id=payload.user_id,
        group_id=payload.group_id,
    )
    
    result = WorkflowStateResultGQLModel(msg = "ok", id = "")
    # result.msg = "ok"
    
    row = next(existing, None)
    
    row = await loader.insert(payload) if row is None else await loader.update(row, {"accesslevel": payload.accesslevel}) or result.update(id=None, msg="fail")
    result.id = payload.workflowstate_id if row else None
    return result


@strawberry.mutation(description="""Remove the user & group from the workflow state""", permission_classes=[OnlyForAuthentized()])
async def workflow_state_remove_user(
    self, info: strawberry.types.Info, payload: WorkflowStateRemoveUserGQLModel
) -> Optional["WorkflowStateResultGQLModel"]:
    
    loader = getLoadersFromInfo(info).workflowstateusers
    
    existing = await loader.filter_by(
        workflowstate_id=payload.workflowstate_id,
        user_id=payload.user_id,
        group_id=payload.group_id,
    )
    
    existing = next(existing, None)
    
    result = WorkflowStateResultGQLModel(msg = "", id = payload.workflowstate_id)
    
    # result.id = payload.workflowstate_id
    result.msg = "fail" if existing is None else (await loader.delete(existing.id), "ok")[1]
    return result
