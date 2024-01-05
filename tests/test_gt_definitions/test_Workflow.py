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


test_reference_workflow = createResolveReferenceTest(
    tableName="awworkflows", gqltype="WorkflowGQLModel"
)
test_query_workflow_page = createPageTest(
    tableName="awworkflows", queryEndpoint="workflowPage", attributeNames=["id"]
)
test_query_workflow_by_id = createByIdTest(
    tableName="awworkflows", queryEndpoint="workflowById", attributeNames=["id"]
)


###     Mutation test


test_insert_workflow = createFrontendQuery(
    query="""mutation($id: UUID! , $name: String!) {
        result: workflowInsert(workflow: {id: $id, name: $name}) {
            id
            msg
        }
    }""",
    variables={"id": "8299eeeb-99e7-4364-8cc2-88b83f900d34" ,"name": "another workflowss"},
   
)


test_update_workflow = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String!, $lastchange: DateTime!){
        result: workflowUpdate(
            workflow: {lastchange: $lastchange, id: $id, name: $name}) {
                id
                msg
                workflow{
                    id
                    name
                    lastchange
                }
            }
        }""",
    variables={"id": "8299eeeb-99e7-4364-8cc2-88b83f900d32" ,"name": "testflow" },
    tableName="awworkflows",
    
)