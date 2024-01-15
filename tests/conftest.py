import os
import re
import json
import pytest
import logging
import fastapi
import uvicorn
from pydantic import BaseModel
from uuid import uuid1 as uuid
import random
import pytest_asyncio

def uuid1():
    return f"{uuid()}"

# serversTestscope = "session"
serversTestscope = "function"

@pytest.fixture
def DBModels():
    from DBDefinitions import (
       WorkflowModel,
       WorkflowStateModel,
       WorkflowStateRoleTypeModel,
       WorkflowStateUserModel,
       WorkflowTransitionModel
    )
    ##
    # order is important!
    ##
    return  [
       WorkflowModel,
       WorkflowStateModel,
       WorkflowStateRoleTypeModel,
       WorkflowStateUserModel,
       WorkflowTransitionModel
        ]

from utils.DBFeeder import get_demodata
@pytest.fixture(scope=serversTestscope)
def DemoData():
    return get_demodata()

@pytest_asyncio.fixture
async def Async_Session_Maker(DBModels):
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker
    from DBDefinitions import BaseModel
    asyncEngine = create_async_engine("sqlite+aiosqlite:///:memory:")
    # asyncEngine = create_async_engine("sqlite+aiosqlite:///data.sqlite")
    async with asyncEngine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async_session_maker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session_maker


@pytest_asyncio.fixture
async def SQLite(Async_Session_Maker, DemoData, DBModels):
    
    from uoishelpers.feeders import ImportModels

    await ImportModels(
        sessionMaker=Async_Session_Maker,
        DBModels=DBModels,
        jsonData=DemoData,
    )    
    logging.info(f"database loaded (SQLite)")
    return Async_Session_Maker

@pytest.fixture
def LoadersContext(SQLite):
    from utils.Dataloaders import createLoadersContext
    context = createLoadersContext(SQLite)
    return context

@pytest.fixture
def Request(AuthorizationHeaders):
    class Request:
        @property
        def headers(self):
            return AuthorizationHeaders
        @property
        def cookies(self):
            return AuthorizationHeaders
        
    return Request()

@pytest.fixture
def Context(AdminUser, SQLite, LoadersContext, Request):
    from utils.gql_ug_proxy import get_ug_connection
    
    Async_Session_Maker = SQLite
    return {
        **LoadersContext,
        "request": Request,
        "": Async_Session_Maker,
        "user": AdminUser,
        "x": "",
        "ug_connection": get_ug_connection
    }

@pytest.fixture
def Request():
    class _Request():
        @property
        def headers(self):
            return {"Authorization": "Bearer 2d9dc5ca-a4a2-11ed-b9df-0242ac120003"}
    return _Request()

@pytest.fixture
def Info(Request, Context):
    class _Info():
        @property
        def context(self):
            context = Context
            context["request"] = Request
            return context

    return _Info()

@pytest.fixture
def QueriesFile():
    file = open("queries.txt", "w+", encoding="utf-8")
    def writequery(query=None, mutation=None, variables={}):
        if (query is not None) and ("mutation" in query):
            jsonData = {
                "query": None,
                "mutation": query,
                "variables": variables
            }
        else:
            jsonData = {
                "query": query,
                "mutation": mutation,
                "variables": variables
            }
        rpattern = r"((?:[a-zA-Z]+Insert)|(?:[a-zA-Z]+Update)|(?:[a-zA-Z]+ById)|(?:[a-zA-Z]+Page))"
        qstring = query if query else mutation
        querynames = re.findall(rpattern, qstring)
        print(querynames)
        queryname = queryname if len(querynames) < 1 else "query_" + querynames[0]
        if jsonData.get("query", None) is None:
            queryname = queryname.replace("query", "mutation")
        queryname = queryname + f"_{query.__hash__()}"
        queryname = queryname.replace("-", "")
        line = f'"{queryname}": {json.dumps(jsonData)}, \n'
        file.write(line)
        pass
    try:
        yield writequery
    finally:
        file.close()

@pytest.fixture
def DemoTrue(monkeypatch):
    print("setting env DEMO to True")
    monkeypatch.setenv("DEMO", "True")
    # import main
    # main.DEMO = True
    yield
    print("end of setting env DEMO to True")

@pytest.fixture
def DemoFalse(monkeypatch):
    print("setting env DEMO to False")
    monkeypatch.setenv("DEMO", "False")
    # import main
    # main.DEMO = True
    yield
    print("end of setting env DEMO to False")

@pytest.fixture
def SchemaExecutor(SQLite, Info):
    from GraphTypeDefinitions import schema
    async def Execute(query, variable_values={}):
        result = await schema.execute(query=query, variable_values=variable_values, context_value=Info.context)
        value = {"data": result.data} 
        if result.errors:
            value["errors"] = result.errors
        return value
    return Execute

@pytest.fixture
def SchemaExecutorDemo(DemoTrue, SchemaExecutor):
    return SchemaExecutor



@pytest.fixture(scope=serversTestscope)
def AdminUser(DemoData):
    users = DemoData["users"]
    user = users[0]
    return {**user, "id": f'{user["id"]}'}

@pytest.fixture
def University(DemoData):
    groups = DemoData["groups"]
    group = next(filter(lambda g: g.get("mastergroup_id", None) is None, groups), None)
    assert group is not None, "group University not found"
    return {**group}

@pytest.fixture
def RoleTypes(DemoData):
    roletypes = DemoData["roletypes"]
    return roletypes

@pytest.fixture
def AllRoleResponse(RoleTypes, AdminUser, University):
    roletypes = RoleTypes
    allRoles = [
        {"user": {**AdminUser}, "group": {**University}, "roletype": {**r}}
        for r in roletypes
    ]

    otherroles = [
        {"user": {"id": uuid1()}, "group": {"id": uuid1()}, "roletype": random.choice(roletypes)}
        for i in range(10)
        ]

    response = {"data": {"result": {"roles": [
        *otherroles,
        *allRoles
    ]}}}

    # print("createRoleResponse.result", response)
    return response

@pytest.fixture
def NoRoleResponse(RoleTypes):
    roletypes = RoleTypes
    otherroles = [
        {"user": {"id": uuid1()}, "group": {"id": uuid1()}, "roletype": random.choice(roletypes)}
        for i in range(10)
        ]

    response = {"data": {"result": {"roles": [
        *otherroles,
    ]}}}
    
    #print("NoRoleResponse.result", response)
    return response

@pytest.fixture
def Env_GQLUG_ENDPOINT_URL_8123(monkeypatch):
    monkeypatch.setenv("GQLUG_ENDPOINT_URL", "http://localhost:8123/gql")
    GQLUG_ENDPOINT_URL = os.environ.get("GQLUG_ENDPOINT_URL", None)
    assert GQLUG_ENDPOINT_URL == "http://localhost:8123/gql", "GQLUG_ENDPOINT_URL setup failed"
    print(f"Env GQLUG_ENDPOINT_URL set to {GQLUG_ENDPOINT_URL}")
    yield ("GQLUG_ENDPOINT_URL", "http://localhost:8123/gql")
    print(f"End of GQLUG_ENDPOINT_URL set to {GQLUG_ENDPOINT_URL}")
    return 

@pytest.fixture(autouse=True) # allrole
def Env_GQLUG_ENDPOINT_URL_8124(monkeypatch):
    # print(40*"GQLUG")
    monkeypatch.setenv("GQLUG_ENDPOINT_URL", "http://localhost:8124/gql")
    GQLUG_ENDPOINT_URL = os.environ.get("GQLUG_ENDPOINT_URL", None)
    assert GQLUG_ENDPOINT_URL == "http://localhost:8124/gql", "GQLUG_ENDPOINT_URL setup failed"
    print(f"Env GQLUG_ENDPOINT_URL set to {GQLUG_ENDPOINT_URL}")
    yield ("GQLUG_ENDPOINT_URL", "http://localhost:8124/gql")
    print(f"End of GQLUG_ENDPOINT_URL set to {GQLUG_ENDPOINT_URL}")
    # print(40*"#")
    return ("GQLUG_ENDPOINT_URL", "http://localhost:8124/gql")

def run(port, response):
    class Item(BaseModel):
        query: str
        variables: dict = None
        operationName: str = None

    app = fastapi.FastAPI()

    @app.post("/gql")
    async def gql_query(item: Item):
        # print("APP queried", item.query)
        #logging.info(f"SERVER Query {item} -> {response}")
        return response
    #print("APP created for", response)

    uvicorn.run(app, port=port)

def runServer(port, response):
    #print(response)
    from multiprocessing import Process
   
    _api_process = Process(target=run, daemon=True, kwargs={"response": response, "port": port})
    _api_process.start()
    print(f"Server started at {port}")
    logging.info(f"Server started at {port}")
    yield _api_process
    _api_process.terminate()
    _api_process.join()
    assert _api_process.is_alive() == False, "Server still alive :("
    print(f"Server stopped at {port}")
    logging.info(f"Server stopped at {port}")


@pytest.fixture(autouse=True, scope=serversTestscope)
def NoRole_UG_Server(NoRoleResponse):
    yield from runServer(port=8123, response=NoRoleResponse)

@pytest.fixture(autouse=True, scope=serversTestscope)
def AllRole_UG_Server(AllRoleResponse):
    yield from runServer(port=8124, response=AllRoleResponse)

def runOAuthServer(port):

    users= [
        {
            "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
            "name": "John",
            "surname": "Newbie",
            "email": "john.newbie@world.com"
        },
        {
            "id": "2d9dc868-a4a2-11ed-b9df-0242ac120003",
            "name": "Julia",
            "surname": "Newbie",
            "email": "julia.newbie@world.com"
        },
        {
            "id": "2d9dc9a8-a4a2-11ed-b9df-0242ac120003",
            "name": "Johnson",
            "surname": "Newbie",
            "email": "johnson.newbie@world.com"
        },
        {
            "id": "2d9dcbec-a4a2-11ed-b9df-0242ac120003",
            "name": "Jepeto",
            "surname": "Newbie",
            "email": "jepeto.newbie@world.com"
        }]

    db_users = [{"id": user["id"], "email": user["email"]} for user in users]

    from mockoauthserver import server as OAuthServer
    mainapp = fastapi.FastAPI()
    app = OAuthServer.createServer(db_users=db_users)
    mainapp.mount("/oauth", app)
    uvicorn.run(mainapp, port=port)

def runOauth(port):
    from multiprocessing import Process
    
    _api_process = Process(target=runOAuthServer, daemon=True, kwargs={"port": port})
    _api_process.start()
    print(f"OAuthServer started at {port}")
    logging.info(f"OAuthServer started at {port}")
    yield _api_process
    _api_process.terminate()
    _api_process.join()
    assert _api_process.is_alive() == False, "Server still alive :("
    print(f"OAuthServer stopped at {port}")
    logging.info(f"OAuthServer stopped at {port}")

@pytest.fixture(scope=serversTestscope)
def OAuthport():
    port = 8125
    return port
    

def runUserInfoServer(port, user):
    from mockoauthserver import server as OAuthServer
    app = fastapi.FastAPI()
    
    @app.get("/oauth/userinfo")
    def getuserinfo():
        return user
    uvicorn.run(app, port=port)

def runUserInfo(port, user):
    from multiprocessing import Process
    
    _api_process = Process(target=runUserInfoServer, daemon=True, kwargs={"port": port, "user": user})
    _api_process.start()
    print(f"UserInfoServer started at {port}")
    logging.info(f"UserInfoServer started at {port}")
    yield _api_process
    _api_process.terminate()
    _api_process.join()

    assert _api_process.is_alive() == False, "Server still alive :("
    print(f"UserInfoServer stopped at {port}")
    logging.info(f"UserInfoServer stopped at {port}")

# @pytest.fixture(scope=serversTestscope)
# def UserInfoServer(monkeypatch, AdminUser):
#     UserInfoServerPort = 8126
#     monkeypatch.setenv("JWTRESOLVEUSERPATHURL", f"http://localhost:{UserInfoServerPort}/oauth/userinfo") #/oauth/publickey
#     logging.info(f"JWTRESOLVEUSERPATHURL set to `http://localhost:{UserInfoServerPort}/oauth/userinfo`")
#     yield from runUserInfo(UserInfoServerPort, AdminUser)

@pytest.fixture(scope=serversTestscope)
def OAuthServer(monkeypatch, OAuthport, AdminUser):
    monkeypatch.setenv("JWTPUBLICKEYURL", f"http://localhost:{OAuthport}/oauth/publickey") #/oauth/publickey
    logging.info(f"JWTPUBLICKEYURL set to `http://localhost:{OAuthport}/oauth/publickey`")
    UserInfoServerPort = 8126
    monkeypatch.setenv("JWTRESOLVEUSERPATHURL", f"http://localhost:{UserInfoServerPort}/oauth/userinfo") #/oauth/publickey
    logging.info(f"JWTRESOLVEUSERPATHURL set to `http://localhost:{UserInfoServerPort}/oauth/userinfo`")

    yield from zip(runOauth(OAuthport), runUserInfo(UserInfoServerPort, AdminUser))


@pytest_asyncio.fixture(autouse=True, scope=serversTestscope)
async def AccessToken(OAuthport, OAuthServer, AdminUser):
    import aiohttp 
    userDict = AdminUser
    # keyurl = f"http://localhost:{OAuthport}/publickey"
    loginurl = f"http://localhost:{OAuthport}/oauth/login3"
    async with aiohttp.ClientSession() as session:
        async with session.get(loginurl) as resp:
            assert resp.status == 200, resp
            accessjson = await resp.json()
        payload = {
            "username": userDict["email"],
            "password": "IDontCare",
            **accessjson
        }
        async with session.post(loginurl, json=payload) as resp:
            assert resp.status == 200, resp
            tokendict = await resp.json()
    token = tokendict["token"] 
    logging.info(f"have token {token}")
    yield token
    logging.info(f"expiring token {token} ")

@pytest_asyncio.fixture
async def AuthorizationHeaders(AccessToken):
    result = {}
    result["authorization"] = f"Bearer {AccessToken}"
    return result


@pytest.fixture
def FastAPIClient(SQLite):
    from fastapi.testclient import TestClient
    import DBDefinitions

    def ComposeCString():
        return "sqlite+aiosqlite:///:memory:"   
    DBDefinitions.ComposeConnectionString = ComposeCString

    import main
    client = TestClient(main.app, raise_server_exceptions=False)   
    return client

@pytest.fixture
def FastAPIClient2():
    from fastapi.testclient import TestClient
    import DBDefinitions

    def ComposeCString():
        return "sqlite+aiosqlite:///:memory:"   
    DBDefinitions.ComposeConnectionString = ComposeCString

    import main
    client = TestClient(main.app, raise_server_exceptions=False)   
    def AcceptHeaders(AuthorizationHeaders):
        async def Execute(query, variable_values={}):
            json = {
                "query": query,
                "variables": variable_values
            }
            headers = AuthorizationHeaders
            logging.debug(f"query client for {query} with {variable_values} and headers {headers}")

            response = client.post("/gql", headers=headers, json=json)
            # assert response.status_code == 200, f"Got no 200 response {response}"
            return response.json()       
        return Execute
    return AcceptHeaders

@pytest.fixture
def FastAPIClient3():
    from fastapi.testclient import TestClient
    import DBDefinitions

    def ComposeCString():
        return "sqlite+aiosqlite:///:memory:"   
    DBDefinitions.ComposeConnectionString = ComposeCString

    import main
    client = TestClient(main.app, raise_server_exceptions=False)   
    def AcceptHeaders(AuthorizationHeaders):
        async def Execute(query, variable_values={}):
            json = {
                "query": query,
                "variables": variable_values
            }
            headers = AuthorizationHeaders
            logging.debug(f"query client for {query} with {variable_values} and headers {headers}")

            response = client.post("/gql2/", headers=headers, json=json)
            assert response.status_code == 200, f"Got no 200 response {response}"
            return response.json()       
        return Execute
    return AcceptHeaders


@pytest_asyncio.fixture(autouse=True, scope=serversTestscope)
async def AccessToken2(OAuthport, OAuthServer):
    async def LoginUser(user):
        import aiohttp 
        userDict = user
        # keyurl = f"http://localhost:{OAuthport}/publickey"
        loginurl = f"http://localhost:{OAuthport}/oauth/login3"
        async with aiohttp.ClientSession() as session:
            async with session.get(loginurl) as resp:
                assert resp.status == 200, resp
                accessjson = await resp.json()
            payload = {
                "username": userDict["email"],
                "password": "IDontCare",
                **accessjson
            }
            async with session.post(loginurl, json=payload) as resp:
                assert resp.status == 200, resp
                tokendict = await resp.json()
        token = tokendict["token"] 
        logging.info(f"have token {token} for {user}")
        return token
    return LoginUser

@pytest_asyncio.fixture
async def ClientExecutorAdmin(FastAPIClient2, AccessToken2, AdminUser):
    logging.info(f"Logged user is {AdminUser}")
    token = await AccessToken2(AdminUser)
    headers = {"authorization": f"Bearer {token}"}
    return FastAPIClient2(headers)

@pytest_asyncio.fixture
async def ClientExecutorNoAdmin(FastAPIClient2, AccessToken2, DemoData):
    table = DemoData["users"]
    user = table[-1]
    logging.info(f"Logged user is {user}")
    token = await AccessToken2(user)
    headers = {"authorization": f"Bearer {token}"}
    return FastAPIClient2(headers)

@pytest_asyncio.fixture
async def ClientExecutorNoAdmin2(FastAPIClient3, AccessToken2, DemoData):
    table = DemoData["users"]
    user = table[-1]
    logging.info(f"Logged user is {user}")
    token = await AccessToken2(user)
    headers = {"authorization": f"Bearer {token}"}
    return FastAPIClient3(headers)


@pytest.fixture
def ClientExecutor(FastAPIClient, AuthorizationHeaders):
    async def Execute(query, variable_values={}):
        json = {
            "query": query,
            "variables": variable_values
        }
        headers = AuthorizationHeaders
        logging.debug(f"query client for {query} with {variable_values} and headers {headers}")

        response = FastAPIClient.post("/gql", headers=headers, json=json)
        # assert response.status_code == 200, f"Got no 200 response {response}"
        return response.json()       
    return Execute

@pytest.fixture
def ClientExecutorDemo(DemoTrue, ClientExecutor):
    return ClientExecutor

@pytest.fixture
def ClientExecutorNoDemo(DemoFalse, ClientExecutor):
    return ClientExecutor
