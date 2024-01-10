import sqlalchemy
import asyncio
import pytest

# from ..uoishelpers.uuid import UUIDColumn


from tests.gqlshared import(
    createByIdTest,
    createPageTest,
    createResolveReferenceTest,
    createFrontendQuery,
    # createRemoveQuery,
    
    )


###     Query test


test_reference_workflowstateuser = createResolveReferenceTest(
    tableName="awworkflowstateusers", gqltype="WorkflowStateUserGQLModel", attributeNames=["id"]
)
test_query_workflowstateuser = createPageTest(
    tableName="awworkflowstateusers", queryEndpoint="workflowStateUser", attributeNames=["id"]
)
test_query_workflowstateuser_by_id = createByIdTest(
    tableName="awworkflowstateusers", queryEndpoint="workflowStateUserById", attributeNames=["id"]
)



###     Mutation test


test_add_workflowstateuser = createFrontendQuery(
    query="""mutation ($wid: UUID!, $uid: UUID!, $gid: UUID!, $al:Int!){
        result: workflowStateAddUser(payload:{workflowstateId: $wid, userId: $uid, groupId: $gid, accesslevel: $al}){
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
    variables={"wid": "eb46ece6-be1b-4142-a5c5-0aac31e681f0", "gid": "f8a46c25-73e2-4d43-bb54-471570be3657", "uid": "f8a46c25-73e2-4d43-bb54-471570be3657", "al": 2},
)



test_remove_workflowstateuser = createFrontendQuery(
    query="""mutation ($workflowstate_id: UUID!, $user_id: UUID!, $groupId: UUID!){
        result: workflowStateRemoveUser(payload:{workflowstateId: $workflowstate_id, userId: $user_id, groupId: $groupId}){
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
    variables={"workflowstate_id": "eb46ece6-be1b-4142-a5c5-0aac31e681f0", "groupId": "f8a46c25-73e2-4d43-bb54-471570be3657", "user_id": "f8a46c25-73e2-4d43-bb54-471570be3657"}
)


