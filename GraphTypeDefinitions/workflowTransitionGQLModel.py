import datetime
import strawberry
from typing import List, Optional, Union, Annotated
import typing
from uuid import UUID
import uuid

from .BaseGQLModel import BaseGQLModel
from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo
from._GraphPermissions import OnlyForAuthentized

from GraphTypeDefinitions._GraphResolvers import (
    resolve_id,
    resolve_lastchange,
    resolve_name,
    resolve_valid,
    createRootResolver_by_id,
    createRootResolver_by_page,
)

UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]
WorkflowGQLModel = Annotated["WorkflowGQLModel", strawberry.lazy(".workflowGQLModel")]
WorkflowStateGQLModel = Annotated[
    "WorkflowStateGQLModel", strawberry.lazy(".workflowStateGQLModel")
]


@strawberry.federation.type(
    keys=["id"], description="""Entity defining a possible state change"""
)
class WorkflowTransitionGQLModel(BaseGQLModel):
    # @classmethod
    # async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
    #     loader = getLoaders(info).workflowtransitions
    #     result = await loader.load(id)
    #     if result is not None:
    #         result._type_definition = cls._type_definition  # little hack :)
    #         result.__strawberry_definition__ = (
    #             cls._type_definition
    #         )  # some version of strawberry changed :(
    #     return result
    
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).workflowtransitions

    id = resolve_id
    name = resolve_name
    valid = resolve_valid
    lastchange = resolve_lastchange

    @strawberry.field(description="""Source""", permission_classes=[OnlyForAuthentized()])
    async def source(
        self, info: strawberry.types.Info
    ) -> Optional[WorkflowStateGQLModel]:
        loader = getLoadersFromInfo(info).workflowstates
        result = await loader.load(self.sourcestate_id)
        return result

    @strawberry.field(description="""Destination""", permission_classes=[OnlyForAuthentized()])
    async def destination(
        self, info: strawberry.types.Info
    ) -> Optional["WorkflowStateGQLModel"]:
        loader = getLoadersFromInfo(info).workflowstates
        result = await loader.load(self.destinationstate_id)
        return result

    @strawberry.field(description="""The owning workflow""", permission_classes=[OnlyForAuthentized()])
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
class WorkflowStateTransitionWhereFilter:
    workflow_id: typing.Optional[uuid.UUID]
    name: str
    sourcestate_id: typing.Optional[uuid.UUID]
    destinationstate_id: typing.Optional[uuid.UUID]


workflow_transition = createRootResolver_by_page(
    scalarType=WorkflowTransitionGQLModel,
    whereFilterType=WorkflowStateTransitionWhereFilter,
    description="Retrieves the transition of workflow",
    loaderLambda=lambda info: getLoadersFromInfo(info).workflowtransitions,
)

workflow_transition_by_id = createRootResolver_by_id(
    WorkflowTransitionGQLModel, description="Retrieves the transition of workflow by id"
)


#####################################################################
#
# Mutation section
#
#####################################################################


@strawberry.input(description="""""")
class WorkflowTransitionInsertGQLModel:
    id: Optional[uuid.UUID] = strawberry.field(
        description="primary key (UUID), could be client generated", default=None
    )
    workflow_id: uuid.UUID = strawberry.field(description="id of workflow")
    name: Optional[str] = None
    name_en: Optional[str] = None
    sourcestate_id: uuid.UUID = strawberry.field(
        default=None, description="Identification of source state"
    )
    destinationstate_id: uuid.UUID = strawberry.field(
        default=None, description="Identification of destination"
    )
    valid: Optional[bool] = True


@strawberry.input(description="""""")
class WorkflowTransitionUpdateGQLModel:
    lastchange: datetime.datetime = strawberry.field(
        description="time of last change = TOKEN"
    )
    id: uuid.UUID = strawberry.field(
        description="primary key (UUID), identifies object of operation"
    )
    sourcestate_id: uuid.UUID = strawberry.field(
        default=None, description="Identification of source state"
    )
    destinationstate_id: uuid.UUID = strawberry.field(
        default=None, description="Identification of destination"
    )
    valid: Optional[bool] = None
    name: Optional[str] = None
    name_en: Optional[str] = None


@strawberry.type(description="""""")
class WorkflowTransitionResultGQLModel:
    id: Optional[uuid.UUID] = strawberry.field(
        description="primary key of CU operation object"
    )
    msg: str = strawberry.field(
        description="""Should be `ok` if descired state has been reached, otherwise `fail`.
    For update operation fail should be also stated when bad lastchange has been entered."""
    )

    @strawberry.field(description="""Result of workflow transition operation""")
    async def transition(
        self, info: strawberry.types.Info
    ) -> WorkflowTransitionGQLModel:
        result = await WorkflowTransitionGQLModel.resolve_reference(info, self.id)
        return result


@strawberry.mutation(description="""Create a new workflow transition""", permission_classes=[OnlyForAuthentized()])
async def workflow_transition_insert(
    self, info: strawberry.types.Info, state: WorkflowTransitionInsertGQLModel
) -> WorkflowTransitionResultGQLModel:
    loader = getLoadersFromInfo(info).workflowtransitions
    row = await loader.insert(state)
    result = WorkflowTransitionResultGQLModel(msg = "ok", id = row.id)
    # result.msg = "ok"
    # result.id = row.id
    return result


@strawberry.mutation(description="""Update a workflow transition""", permission_classes=[OnlyForAuthentized()])
async def workflow_transition_update(
    self, info: strawberry.types.Info, state: WorkflowTransitionUpdateGQLModel
) -> WorkflowTransitionResultGQLModel:
    loader = getLoadersFromInfo(info).workflowtransitions
    row = await loader.update(state)
    result = WorkflowTransitionResultGQLModel(msg = "ok", id = state.id)
    # result.msg = "ok"
    # result.id = state.id
    if row is None:
        result.msg = "fail"

    return result
