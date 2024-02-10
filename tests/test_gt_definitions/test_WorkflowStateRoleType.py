import sqlalchemy
import asyncio
import pytest

# from ..uoishelpers.uuid import UUIDColumn



# from tests.gqlshared import (
#     createByIdTest, 
#     createPageTest, 
#     createResolveReferenceTest,
#     createFrontendQuery,
#     createUpdateQuery,
    
#     )

from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery,
    createDeleteQuery
)


###     Query test


test_reference_workflowstateroletype = createResolveReferenceTest(
    tableName="awworkflowstateroletypes", gqltype="WorkflowStateRoleTypeGQLModel", attributeNames=["id"]
)
test_query_workflowstateroletype = createPageTest(
    tableName="awworkflowstateroletypes", queryEndpoint="workflowStateRoleType", attributeNames=["id"]
)
test_query_workflowstateroletype_by_id = createByIdTest(
    tableName="awworkflowstateroletypes", queryEndpoint="workflowStateRoleTypeById", attributeNames=["id"]
)


###     Mutation test

test_add_workflowstateroletype = createFrontendQuery(
    query="""mutation ($wid: UUID!, $rid: UUID!, $al:Int!){
        result: workflowStateAddRole(payload:{workflowstateId: $wid, roletypeId: $rid, accesslevel: $al}){
            id
            msg
            state{
                id
                name
                lastchange
                roletypes{
                    id
                    accesslevel
                    roleType{
                        id
                    }
                }
            }
        }
    }""",
    variables={"wid": "eb46ece6-be1b-4142-a5c5-0aac31e681f0", "rid": "f8a46c25-73e2-4d43-bb54-471570be3657", "al": 2}
)

test_remove_workflowstateroletype = createFrontendQuery(
    query="""mutation ($wid: UUID!, $rid: UUID!) {
        result: workflowStateRemoveRole(payload: {workflowstateId: $wid, roletypeId: $rid}) {
                    id
                    msg
                }
        }""",
    variables={"wid": "eb46ece6-be1b-4142-a5c5-0aac31e681f0", "rid": "f8a46c25-73e2-4d43-bb54-471570be3657"}
)


# test_remove_workflowstateroletype = createDeleteQuery(tableName= "awworkflowstateroletypes", 
#                                                       queryBase="workflowState", 
#                                                       id="c7dffbfd-48eb-416f-9bf6-0f0ff6fef44f")


