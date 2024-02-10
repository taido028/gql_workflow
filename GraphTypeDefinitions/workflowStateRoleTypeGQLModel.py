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
    resolve_accesslevel,
    resolve_createdby,
    resolve_changedby,
    resolve_rbacobject,
    createRootResolver_by_id,
    createRootResolver_by_page,
)

from GraphTypeDefinitions.workflowStateGQLModel import (
    WorkflowStateResultGQLModel,
    
)

WorkflowGQLModel = Annotated["WorkflowGQLModel", strawberry.lazy(".workflowGQLModel")]
WorkflowStateGQLModel = Annotated[
    "WorkflowStateGQLModel", strawberry.lazy(".workflowStateGQLModel")
]
# WorkflowStateResultGQLModel = Annotated[
#     "WorkflowStateResultGQLModel", strawberry.lazy(".workflowStateGQLModel")
# ]
RoleTypeGQLModel = Annotated["RoleTypeGQLModel", strawberry.lazy(".externals")]


@strawberry.federation.type(
    keys=["id"],
    description="""Entity defining role types with some rights for the state in dataflow (node in graph)""",
)
class WorkflowStateRoleTypeGQLModel(BaseGQLModel):
    # async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
    #     loader = getLoaders(info).workflowstateusers
    #     result = await loader.load(id)
    #     if result is not None:
    #         result._type_definition = cls._type_definition  # little hack :)
    #         result.__strawberry_definition__ = (
    #             cls._type_definition
    #         )  # some version of strawberry changed :(
    #     return result

    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).workflowstateroletypes

    id = resolve_id
    lastchange = resolve_lastchange
    accesslevel = resolve_accesslevel
    rbacobject = resolve_rbacobject
    valid = resolve_valid


    @strawberry.field(description="""State""", permission_classes=[OnlyForAuthentized()])
    async def state(
        self, info: strawberry.types.Info
    ) -> Optional["WorkflowStateGQLModel"]:
        loader = getLoadersFromInfo(info).workflowstates
        result = await loader.load(self.workflowstate_id)
        return result

    @strawberry.field(description="""Role type with some rights""", permission_classes=[OnlyForAuthentized()])
    def role_type(self) -> Optional["RoleTypeGQLModel"]:
        from .externals import RoleTypeGQLModel

        return RoleTypeGQLModel(id=self.roletype_id)


#####################################################################
#
# Special fields for query
#
#####################################################################


from dataclasses import dataclass
from uoishelpers.resolvers import createInputs


@createInputs
@dataclass
class WorkflowStateRoleTypeWhereFilter:
    workflowstate_id: typing.Optional[uuid.UUID]
    roletype_id: typing.Optional[uuid.UUID]
    accesslevel: int
    valid : bool
    created: datetime.datetime
    createdby: UUID
    changedby: UUID

    from .workflowStateGQLModel import WorkflowStateWhereFilter
    
    states: WorkflowStateWhereFilter


workflow_state_role_type = createRootResolver_by_page(
    scalarType=WorkflowStateRoleTypeGQLModel,
    whereFilterType=WorkflowStateRoleTypeWhereFilter,
    description="""Returns roletype of workflow states by page""",
    loaderLambda=lambda info: getLoadersFromInfo(info).workflowstateroletypes,
)


workflow_state_role_type_by_id = createRootResolver_by_id(
    WorkflowStateRoleTypeGQLModel,
    description="""Returns workflow state roletype by ID""",
)


#####################################################################
#
# Mutation section
#
#####################################################################


@strawberry.input(description="""Input structure - C and U operation""")
class WorkflowStateAddRoleGQLModel:
    workflowstate_id: uuid.UUID = strawberry.field(
        default=None, description="Identification of workflow state"
    )
    roletype_id: uuid.UUID = strawberry.field(
        default=None, description="Identification of role type"
    )
    accesslevel: int = strawberry.field(description="access level")
    valid: Optional[bool] = True
    createdby: strawberry.Private[UUID] = None


@strawberry.input(description=""" D operation""")
class WorkflowStateRemoveRoleGQLModel:
    workflowstate_id: UUID = strawberry.field(
        default=None, description="Identification of workflow state"
    )
    roletype_id: UUID = strawberry.field(
        default=None, description="Identification of role type"
    )

@strawberry.mutation(description="""Adds or updates role at the workflow state""", permission_classes=[OnlyForAuthentized()])
async def workflow_state_add_role(
    self, info: strawberry.types.Info, payload: WorkflowStateAddRoleGQLModel
) -> Optional["WorkflowStateResultGQLModel"]:
    
    loader = getLoadersFromInfo(info).workflowstateroletypes
    
    existing = await loader.filter_by(
        workflowstate_id=payload.workflowstate_id,
        roletype_id=payload.roletype_id,
    )
    
    result = WorkflowStateResultGQLModel(msg = "ok", id = "")
    
    # result.msg = "ok"
    
    row = next(existing, None)
    
    row = await loader.insert(payload) if row is None else await loader.update(row, {"accesslevel": payload.accesslevel}) or result.update(id=None, msg="fail")
    result.id = payload.workflowstate_id if row else None
    return result


@strawberry.mutation(description="""Remove the role from the workflow state""", permission_classes=[OnlyForAuthentized()])
async def workflow_state_remove_role(
    self, info: strawberry.types.Info, payload: WorkflowStateRemoveRoleGQLModel
) -> Optional["WorkflowStateResultGQLModel"]:
    
    loader = getLoadersFromInfo(info).workflowstateroletypes
    
    existing = await loader.filter_by(
        workflowstate_id = payload.workflowstate_id, 
        roletype_id = payload.roletype_id,
    )
    
    existing = next(existing, None)
    
    result = WorkflowStateResultGQLModel(id = payload.workflowstate_id, msg = "ok")
    # result.id = payload.workflowstate_id
    
    result.msg = "fail" if existing is None else (await loader.delete(existing.id), "ok")[1]
    return result
