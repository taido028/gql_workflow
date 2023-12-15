import logging
import json

def createGQLClient():

    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    import gql_workflow.DBDefinitions

    def ComposeCString():
        return "sqlite+aiosqlite:///:memory:"
    
    gql_workflow.DBDefinitions.ComposeConnectionString = ComposeCString

    import main
    
    client = TestClient(main.app, raise_server_exceptions=False)
    
    return client

def CreateClientFunction():
    client = createGQLClient()

    async def result(query, variables={}):
        json = {
            "query": query,
            "variables": variables
        }
        headers = {"Authorization": "Bearer 2d9dc5ca-a4a2-11ed-b9df-0242ac120003"}
        logging.debug(f"query client for {query} with {variables}")

        response = client.post("/gql", headers=headers, json=json)
        return response.json()
    
    return result

def updateIntrospectionQuery():
    from .introspection import query
    client = createGQLClient()
    inputjson = {"query": query, "variables": {}}
    response = client.post("/gql", headers={}, json=inputjson)
    responsejson = response.json()
    data = responsejson["data"]
    print(responsejson)
    with open("./introspectionquery.json", "w", encoding="utf-8") as f:
        datastr = json.dumps(data)
        f.write(datastr)

updateIntrospectionQuery()