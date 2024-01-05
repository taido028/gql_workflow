import sqlalchemy
import asyncio
import pytest

# from ..uoishelpers.uuid import UUIDColumn




from tests.gqlshared import( 
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest,
    createFrontendQuery,
    createUpdateQuery,
    
    )


###     Query test

test_reference_workflowstate = createResolveReferenceTest(
    tableName="awworkflowstates", gqltype="WorkflowStateGQLModel"
)
test_query_workflowstate = createPageTest(
    tableName="awworkflowstates", queryEndpoint="workflowState", attributeNames=["id"]
)
test_query_workflowstate_by_id = createByIdTest(
    tableName="awworkflowstates", queryEndpoint="workflowStateById", attributeNames=["id"]
)


###     Muatation test

test_insert_workflowstate = createFrontendQuery(
    query="""mutation ($workflowId:UUID!, $name:String!){
        result: workflowStateInsert(state:{workflowId: $workflowId, name: $name}){
            id
            msg
            state{
                id
                name
            }
        }
    }""",
    variables={"workflowId":"8299eeeb-99e7-4364-8cc2-88b83f900d34", "name": "test name" },
    
)


test_update_workflowstate = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String!, $lastchange: DateTime!){
        result: workflowStateUpdate(state:{lastchange: $lastchange, id: $id, name: $name}) {
            id
            msg
            state {
                id
                name
                lastchange
            }
        }
    }""",
    variables={"id": "eb46ece6-be1b-4142-a5c5-0aac31e681f0", "name": "StudentX" },
    tableName="awworkflowstates",
    
)