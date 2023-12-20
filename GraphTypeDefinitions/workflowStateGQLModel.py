import datetime
import strawberry
from typing import List, Optional, Union, Annotated
import typing
import uuid
from uuid import UUID

from sqlalchemy.util import typing
from GraphTypeDefinitions.BaseGQLModel import BaseGQLModel
from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

from GraphTypeDefinitions._GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_valid,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby,
    createRootResolver_by_id,
    createRootResolver_by_page,
)


UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]
WorkflowGQLModel = Annotated["WorkflowGQLModel", strawberry.lazy(".workflowGQLModel")]
WorkflowTransitionGQLModel = Annotated[
    "WorkflowTransitionGQLModel", strawberry.lazy(".workflowTransitionGQLModel")
]
WorkflowStateUserGQLModel = Annotated[
    "WorkflowStateUserGQLModel", strawberry.lazy(".workflowStateUserGQLModel")
]
WorkflowStateRoleTypeGQLModel = Annotated[
    "WorkflowStateRoleTypeGQLModel", strawberry.lazy(".workflowStateRoleTypeGQLModel")
]


@strawberry.federation.type(
    keys=["id"], description="""Entity defining a state in dataflow (node in graph)"""
)
class WorkflowStateGQLModel(BaseGQLModel):
    # async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
    #     loader = getLoaders(info).workflowstates
    #     result = await loader.load(id)
    #     if result is not None:
    #         result._type_definition = cls._type_definition  # little hack :)
    #         result.__strawberry_definition__ = (
    #             cls._type_definition
    #         )  # some version of strawberry changed :(
    #     return result
    
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).workflowstates

    id = resolve_id
    name = resolve_name
    valid = resolve_valid
    lastchange = resolve_lastchange
    createdby = resolve_createdby
    changedby = resolve_changedby

    @strawberry.field(description="""outcomming transitions""")
    async def next_transitions(
        self, info: strawberry.types.Info
    ) -> List["WorkflowTransitionGQLModel"]:
        loader = getLoadersFromInfo(info).workflowtransitions
        result = await loader.filter_by(sourcestate_id=self.id)
        return result

    @strawberry.field(description="""incomming transitions""")
    async def previous_transitions(
        self, info: strawberry.types.Info
    ) -> List["WorkflowTransitionGQLModel"]:
        loader = getLoadersFromInfo(info).workflowtransitions
        result = await loader.filter_by(destinationstate_id=self.id)
        return result

    @strawberry.field(description="""User rights""")
    async def users(
        self, info: strawberry.types.Info
    ) -> List["WorkflowStateUserGQLModel"]:
        loader = getLoadersFromInfo(info).workflowstateusers
        result = await loader.filter_by(workflowstate_id=self.id)
        return result

    @strawberry.field(description="""User rights""")
    async def roletypes(
        self, info: strawberry.types.Info
    ) -> List["WorkflowStateRoleTypeGQLModel"]:
        loader = getLoadersFromInfo(info).workflowstateroletypes
        result = await loader.filter_by(workflowstate_id=self.id)
        return result

    @strawberry.field(description="""The owning workflow""")
    async def workflow(
        self, info: strawberry.types.Info
    ) -> Optional["WorkflowGQLModel"]:
        loader = getLoadersFromInfo(info).workflows
        result = await loader.load(self.workflow_id)
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
class WorkflowStateWhereFilter:
    workflow_id: typing.Optional[uuid.UUID]
    name: str


workflow_state_by_id = createRootResolver_by_id(
    WorkflowStateGQLModel, description="Retrieves the workflow by id"
)

workflow_state = createRootResolver_by_page(
    scalarType=WorkflowStateGQLModel,
    whereFilterType=WorkflowStateWhereFilter,
    description="Retrieves the workflow",
    loaderLambda=lambda info: getLoadersFromInfo(info).workflowstates,
)

#####################################################################
#
# Mutation section
#
#####################################################################


@strawberry.input
class WorkflowStateInsertGQLModel:
    id: Optional[uuid.UUID] = strawberry.field(
        description="primary key (UUID), could be client generated", default=None
    )
    workflow_id: uuid.UUID = strawberry.field(description="id of workflow")
    name: Optional[str] = None
    name_en: Optional[str] = None
    valid: Optional[bool] = True


@strawberry.input
class WorkflowStateUpdateGQLModel:
    lastchange: datetime.datetime = strawberry.field(
        description="time of last change = TOKEN"
    )
    id: uuid.UUID = strawberry.field(
        description="primary key (UUID), identifies object of operation"
    )
    valid: Optional[bool] = None
    name: Optional[str] = None
    name_en: Optional[str] = None


@strawberry.type
class WorkflowStateResultGQLModel:
    id: Optional[uuid.UUID] = strawberry.field(
        description="primary key of CU operation object"
    )
    msg: str = strawberry.field(
        description="""Should be `ok` if descired state has been reached, otherwise `fail`.
    For update operation fail should be also stated when bad lastchange has been entered."""
    )

    @strawberry.field(description="""Result of workflow state operation""")
    async def state(self, info: strawberry.types.Info) -> WorkflowStateGQLModel:
        result = await WorkflowStateGQLModel.resolve_reference(info, self.id)
        return result


@strawberry.mutation(description="Create a new state of workflow")
async def workflow_state_insert(
    self, info: strawberry.types.Info, state: WorkflowStateInsertGQLModel
) -> WorkflowStateResultGQLModel:
    loader = getLoadersFromInfo(info).workflowstates
    row = await loader.insert(state)
    result = WorkflowStateResultGQLModel(id=row.id, msg="ok")

    return result


@strawberry.mutation
async def workflow_state_update(
    self, info: strawberry.types.Info, state: WorkflowStateUpdateGQLModel
) -> WorkflowStateResultGQLModel:
    loader = getLoadersFromInfo(info).workflowstates
    row = await loader.update(state)
    result = WorkflowStateResultGQLModel(id=row.id, msg="ok")
    if row is None:
        result.msg = "fail"

    return result
