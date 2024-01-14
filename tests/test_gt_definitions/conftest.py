import logging
import datetime
import pytest_asyncio
import uuid

@pytest_asyncio.fixture
async def GQLInsertQueries():
    result = {
        "awworkflows": {
            "create": """
mutation ($id: UUID! , $name: String!) {
  workflowInsert(
    workflow: {id: $id, name: $name}
  ) {
    id
    msg
  }
}""",
            "read": """query($id: UUID!){ result: workflowById(id: $id) { id }}""",
},
        "awworkflowstates": {"create": """
mutation ($workflowId:UUID!, $name:String!) {
  workflowStateInsert(
    state: {workflowId: $workflowId, name: $name}
  ) {
    id
    msg
  }
}""",
            "read": """query($id: UUID!){ result: workflowStateById(id: $id) { id }}""",
},
        "awworkflowstateroletypes":{"create": """
mutation ($wid: UUID!, $rid: UUID!, $al:Int!) {
  workflowStateAddRole(
    payload: {workflowstateId: $wid, roletypeId: $rid, accesslevel: $al}
  ) {
    id
    msg
  }
}""",
            "read": """query($id: UUID!){ result: workflowStateRoleTypeById(id: $id) { id }}""",
},
        "awworkflowstateusers": {"create": """
mutation ($wid: UUID!, $uid: UUID!, $gid: UUID!, $al:Int!) {
  workflowStateAddUser(
    payload: {workflowstateId: $wid, userId: $uid, groupId: $gid, accesslevel: $al}
  ) {
    id
    msg
  }
}""",
            "read": """query($id: UUID!){ result: workflowStateUserById(id: $id) { id }}""",
},
        "awworkflowtransitions": {"create": """
mutation ($workflowId: UUID!, $name: String!, $sid: UUID!, $did: UUID!) {
  workflowTransitionInsert(
    state: {workflowId: $workflowId, name: $name, sourcestateId: $sid, destinationstateId: $did}
  ) {
    id
    msg
  }
}""",
            "read": """query($id: UUID!){ result: workflowTransitionById(id: $id) { id }}""",
},
#         "events_users": {"create": """
# mutation ($user_id: UUID!, $event_id: UUID!, $invitationtype_id: UUID!, $presencetype_id: UUID!) {
#   presenceInsert(
#     presence: {userId: $user_id, eventId: $event_id, invitationtypeId: $invitationtype_id, presencetypeId: $presencetype_id}
#   ) {
#     id
#     msg
#   }
# }""",
#             "read": """query($id: UUID!){ result: presenceById(id: $id) { id }}""",
# },
#       "eventpresencetypes": {"create": """
# mutation ($id: UUID!, $name: String!) {
#   presenceTypeInsert(
#     presenceType: {id: $id, name: $name}
#   ) {
#     id
#     msg
#   }
# }""",
#             "read": """query($id: UUID!){ result: presenceTypeById(id: $id) { id }}""",
# },

    }
    
    return result


@pytest_asyncio.fixture
async def FillDataViaGQL(DemoData, GQLInsertQueries, ClientExecutorAdmin):
    types = [type(""), type(datetime.datetime.now()), type(uuid.uuid1())]
    for tablename, queryset in GQLInsertQueries.items():
        table = DemoData.get(tablename, None)
        assert table is not None, f"{tablename} is missing in DemoData"

        for row in table:
            variable_values = {}
            for key, value in row.items():
                variable_values[key] = value
                if isinstance(value, datetime.datetime):
                    variable_values[key] = value.isoformat()
                elif type(value) in types:
                    variable_values[key] = f"{value}"

            readResponse = await ClientExecutorAdmin(query=queryset["read"], variable_values=variable_values)
            if readResponse["data"]["result"] is not None:
                logging.info(f"row with id `{variable_values['id']}` already exists in `{tablename}`")
                continue
            insertResponse = await ClientExecutorAdmin(query=queryset["create"], variable_values=variable_values)
            assert insertResponse.get("errors", None) is None, insertResponse
        logging.info(f"{tablename} initialized via gql query")
    logging.info(f"All WANTED tables are initialized")