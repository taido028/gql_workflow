import sqlalchemy
import asyncio
import pytest

# from ..uoishelpers.uuid import UUIDColumn

from gql_workflow.GraphTypeDefinitions import schema

from tests.shared import (
    prepare_demodata,
    prepare_in_memory_sqllite,
    get_demodata,
    createContext,
)

from tests.gqlshared import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest
)

###     Query test


test_reference_workflow = createResolveReferenceTest(tableName="awworkflows", gqltype="WorkflowGQLModel")
test_query_workflow_page = createPageTest(tableName="awworkflows", queryEndpoint="workflowPage")
test_query_workflow_by_id = createByIdTest(tableName="awworkflows", queryEndpoint="workflowById")



###     Mutation test

@pytest.mark.asyncio
async def test_workflow_mutation():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    
    table = data["awworkflows"]
    row = table[0]
    user_id = row["id"]


    name = "workflow X"
    query = '''
            mutation(
                $name: String!
                
                ) {
                operation: workflowInsert(workflow: {
                    name: $name
                    
                }){
                    id
                    msg
                    entity: workflow {
                        id
                        name
                        lastchange
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    variable_values = {
        "name": name
    }
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    
    print(resp, flush=True)

    assert resp.errors is None
    data = resp.data['operation']
    assert data["msg"] == "ok"
    data = data["entity"]
    assert data["name"] == name
    
    #assert data["name"] == name
    
   
    id = data["id"]
    lastchange = data["lastchange"]
    name = "NewName"
    query = '''
            mutation(
                $id: UUID!,
                $lastchange: DateTime!
                $name: String!
                ) {
                operation: workflowUpdate(workflow: {
                id: $id,
                lastchange: $lastchange
                name: $name
            }){
                id
                msg
                entity: workflow {
                    id
                    name
                    lastchange
                }
            }
            }
        '''
    newName = "newName"
    context_value = await createContext(async_session_maker)
    variable_values = {"id": id, "name": newName, "lastchange": lastchange}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None

    data = resp.data['operation']
    assert data['msg'] == "ok"
    data = data["entity"]
    assert data["name"] == newName

    # lastchange je jine, musi fail
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    data = resp.data['operation']
    assert data['msg'] == "fail"

    pass