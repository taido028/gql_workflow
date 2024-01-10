import sqlalchemy
import asyncio
import pytest

# from ..uoishelpers.uuid import UUIDColumn




from tests.gqlshared import (
    createByIdTest,
    createPageTest,
    createResolveReferenceTest,
    createFrontendQuery,
    createUpdateQuery,
    
)

###     Query test


test_reference_workflowtransition = createResolveReferenceTest(
    tableName="awworkflowtransitions", gqltype="WorkflowTransitionGQLModel", attributeNames=["id"]
)

test_query_workflowtransition_by_id = createByIdTest(
    tableName="awworkflowtransitions", queryEndpoint="workflowTransitionById", attributeNames=["id"]
)

test_query_workflowtransition = createPageTest(
    tableName="awworkflowtransitions", queryEndpoint="workflowTransition", attributeNames=["id"]
)


###     Mutation test


test_insert_workflowtransition = createFrontendQuery(
    query="""mutation ($workflowId: UUID!, $name: String!, $sid: UUID!, $did: UUID!){
        result: workflowTransitionInsert(state:{workflowId: $workflowId, name: $name, sourcestateId: $sid, destinationstateId: $did}){
            id
            msg
            transition{
                id
            }
        }
    }""",
    variables={"workflowId": "eb46ece6-be1b-4142-a5c5-0aac31e681f0", "name": "test", "sid": "f8a46c25-73e2-4d43-bb54-471570be3657", "did": "f8a46c25-73e2-4d43-bb54-471570be3657",}
)

test_update_workflowtransition = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String!, $sourcestateId: UUID!, $destinationstateId: UUID!, $lastchange: DateTime!){
        result: workflowTransitionUpdate(state:{id: $id, name: $name, sourcestateId: $sourcestateId, destinationstateId: $destinationstateId, lastchange: $lastchange}){
            id
            msg
            transition{
                id
                lastchange
            }
        }
    }""",
    variables={"id": "22b0aec9-a0d4-4a8b-a34d-6481fe45f14b", "name": "test", "sourcestateId": "eb46ece6-be1b-4142-a5c5-0aac31e681f0", "destinationstateId": "31b95aba-4de0-43f5-91ec-ba69183b1ffe"},
    tableName="awworkflowtransitions",
)