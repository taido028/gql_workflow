import uuid
import datetime
import strawberry
from typing import List, Optional, Union, Annotated
from uuid import UUID

from .BaseGQLModel import BaseGQLModel
from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo
from ._GraphPermissions import OnlyForAuthentized

from GraphTypeDefinitions._GraphResolvers import (
    resolve_id,
    resolve_lastchange,
    resolve_name,
    resolve_valid,
    resolve_created,
    resolve_createdby,
    resolve_changedby,
    resolve_rbacobject,
    createRootResolver_by_id,
    createRootResolver_by_page,
    
)


WorkflowTransitionGQLModel = Annotated[
    "WorkflowTransitionGQLModel", strawberry.lazy(".workflowTransitionGQLModel")
]
WorkflowStateUserGQLModel = Annotated[
    "WorkflowStateUserGQLModel", strawberry.lazy(".workflowStateUserGQLModel")
]
WorkflowStateGQLModel = Annotated[
    "WorkflowStateGQLModel", strawberry.lazy(".workflowStateGQLModel")
]


@strawberry.federation.type(
    keys=["id"], name="WorkflowGQLModel", description="""Entity graph of dataflow"""
)
class WorkflowGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).workflows

    id = resolve_id
    name = resolve_name
    lastchange = resolve_lastchange    
    created = resolve_created
    

    @strawberry.field(description="""Proxy states attached to this workflow""", permission_classes=[OnlyForAuthentized(isList=True)] )
    async def states(
        self, info: strawberry.types.Info
    ) -> List["WorkflowStateGQLModel"]:
        loader = getLoadersFromInfo(info).workflowstates
        result = await loader.filter_by(workflow_id=self.id)
        return result

    @strawberry.field(description="""Proxy transitions attached to this workflow""", permission_classes=[OnlyForAuthentized(isList=True)])
    async def transitions(
        self, info: strawberry.types.Info
    ) -> List["WorkflowTransitionGQLModel"]:
        loader = getLoadersFromInfo(info).workflowtransitions
        result = await loader.filter_by(workflow_id=self.id)
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
class WorkflowWhereFilter:
    id: UUID
    name: str
    valid: bool
    created: datetime.datetime
    createdby: UUID
    changedby: UUID


workflow_by_id = createRootResolver_by_id(
    WorkflowGQLModel, description="Retrieves the workflow by id"
)

workflow_page = createRootResolver_by_page(
    scalarType=WorkflowGQLModel,
    whereFilterType=WorkflowWhereFilter,
    description="Retrieves the workflow paged",
    loaderLambda=lambda info: getLoadersFromInfo(info).workflows,
)


#####################################################################
#
# Mutation section
#
#####################################################################
from ._GraphPermissions import OnlyForAuthentized

@strawberry.input(description="""Definition of workflow added to entity""")
class WorkflowInsertGQLModel:
    name: str = strawberry.field(description="workflow name")
    name_en: Optional[str] = strawberry.field(
        default=None, description="En name of type"
    )
    id: Optional[UUID] = strawberry.field(description="""primary key (UUID)""")
    valid: Optional[bool] = True
    createdby: strawberry.Private[UUID] = None


@strawberry.input()
class WorkflowUpdateGQLModel:
    lastchange: datetime.datetime = strawberry.field(
        description="timestamp of last change = TOKEN"
    )
    id: uuid.UUID = strawberry.field(description="""primary key (UUID)""")
    name: Optional[str] = None
    name_en: Optional[str] = None
    valid: Optional[bool] = None
    changedby: strawberry.Private[UUID] = None


@strawberry.type
class WorkflowResultGQLModel:
    id: Optional[UUID] = strawberry.field(
        default=None, description="Primary key of table row"
    )
    msg: str = strawberry.field(
        default=None, description="""result of operation, should be "ok" or "fail" """
    )

    @strawberry.field(description="""Result of workflow operation""")
    async def workflow(
        self, info: strawberry.types.Info
    ) -> Union[WorkflowGQLModel, None]:
        result = await WorkflowGQLModel.resolve_reference(info, self.id)
        return result


@strawberry.mutation(description="""Creates a new workflow""", permission_classes=[OnlyForAuthentized()])
async def workflow_insert(
    self, info: strawberry.types.Info, workflow: WorkflowInsertGQLModel
) -> WorkflowResultGQLModel:
    user = getUserFromInfo(info)
    workflow.createdby = UUID(user["id"])
    loader = getLoadersFromInfo(info).workflows
    row = await loader.insert(workflow)
    result = WorkflowResultGQLModel(id=row.id, msg="ok")

    return result


@strawberry.mutation(description="""Updates a new workflow""", permission_classes=[OnlyForAuthentized()])
async def workflow_update(
    self, info: strawberry.types.Info, workflow: WorkflowUpdateGQLModel
) -> WorkflowResultGQLModel:
    user = getUserFromInfo(info)
    workflow.changedby = UUID(user["id"])
    loader = getLoadersFromInfo(info).workflows

    row = await loader.update(workflow)
    result = WorkflowResultGQLModel(id=workflow.id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    return result
