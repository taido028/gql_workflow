# from typing import List, Any
# import typing
# import os
# from pydantic import BaseModel


# import asyncio

# from fastapi import FastAPI, Request
# import strawberry
# from strawberry.fastapi import GraphQLRouter

# ## Definice GraphQL typu (pomoci strawberry https://strawberry.rocks/)
# ## Strawberry zvoleno kvuli moznosti mit federovane GraphQL API (https://strawberry.rocks/docs/guides/federation, https://www.apollographql.com/docs/federation/)

# ## Definice DB typu (pomoci SQLAlchemy https://www.sqlalchemy.org/)
# ## SQLAlchemy zvoleno kvuli moznost komunikovat s DB asynchronne
# ## https://docs.sqlalchemy.org/en/14/core/future.html?highlight=select#sqlalchemy.future.select
# from DBDefinitions import startEngine, ComposeConnectionString

# ## Zabezpecuje prvotni inicializaci DB a definovani Nahodne struktury pro "Univerzity"
# # from gql_workflow.DBFeeder import createSystemDataStructureRoleTypes, createSystemDataStructureGroupTypes
# connectionString = ComposeConnectionString()

# from strawberry.asgi import GraphQL
# from utils.Dataloaders import createLoaders
# import logging

# appcontext = {}

# from contextlib import asynccontextmanager


# import logging
# import logging.handlers
# import socket
# logging.basicConfig(
#     level=logging.INFO, 
#     format='%(asctime)s.%(msecs)03d\t%(levelname)s:\t%(message)s', 
#     datefmt='%Y-%m-%dT%I:%M:%S')
# SYSLOGHOST = os.getenv("SYSLOGHOST", None)
# if SYSLOGHOST is not None:
#     [address, strport, *_] = SYSLOGHOST.split(':')
#     assert len(_) == 0, f"SYSLOGHOST {SYSLOGHOST} has unexpected structure, try `localhost:514` or similar (514 is UDP port)"
#     port = int(strport)
#     my_logger = logging.getLogger()
#     my_logger.setLevel(logging.INFO)
#     handler = logging.handlers.SysLogHandler(address=(address, port), socktype=socket.SOCK_DGRAM)
#     #handler = logging.handlers.SocketHandler('10.10.11.11', 611)
#     my_logger.addHandler(handler)
    


# from fastapi import FastAPI, Request, Depends
# from strawberry.fastapi import GraphQLRouter
# from contextlib import asynccontextmanager

# from DBDefinitions import ComposeConnectionString

# ## Zabezpecuje prvotni inicializaci DB a definovani Nahodne struktury pro "Univerzity"
# # from gql_workflow.DBFeeder import createSystemDataStructureRoleTypes, createSystemDataStructureGroupTypes

# connectionString = ComposeConnectionString()



# appcontext = {}
# @asynccontextmanager
# async def initEngine(app: FastAPI):

#     from DBDefinitions import startEngine, ComposeConnectionString

#     connectionstring = ComposeConnectionString()
#     makeDrop = os.getenv("DEMO", None) == "True"
#     asyncSessionMaker = await startEngine(
#         connectionstring=connectionstring,
#         makeDrop=makeDrop,
#         makeUp=True
#     )

#     appcontext["asyncSessionMaker"] = asyncSessionMaker

#     logging.info("engine started")

#     from utils.DBFeeder import initDB
#     await initDB(asyncSessionMaker)

#     logging.info("data (if any) imported")
#     yield





# from GraphTypeDefinitions import schema
# from utils.sentinel import sentinel

# app = FastAPI(lifespan=initEngine)



# # class Item(BaseModel):
# #     query: str
# #     variables: dict = {}
# #     operationName: str = None


# # async def get_context(request: Request):
# #     asyncSessionMaker = appcontext.get("asyncSessionMaker", None)
# #     if asyncSessionMaker is None:
# #         async with initEngine(app) as cntx:
# #             pass
        
# #     from utils.Dataloaders import createLoadersContext, createUgConnectionContext
# #     context = createLoadersContext(appcontext["asyncSessionMaker"])
# #     i = Item(query = "")
# #     # i.query = ""
# #     # i.variables = {}
# #     logging.info(f"before sentinel current user is {request.scope.get('user', None)}")
# #     await sentinel(request, i)
# #     logging.info(f"after sentinel current user is {request.scope.get('user', None)}")
# #     connectionContext = createUgConnectionContext(request=request)
# #     result = {**context, **connectionContext}
# #     result["request"] = request
# #     result["user"] = request.scope.get("user", None)
# #     logging.info(f"context created {result}")
# #     return result



# async def get_context():
#     asyncSessionMaker = appcontext.get("asyncSessionMaker", None)
#     if asyncSessionMaker is None:
#         async with initEngine(app) as cntx:
#             pass

#     from utils.Dataloaders import createLoadersContext

#     context = createLoadersContext(appcontext["asyncSessionMaker"])
#     return context



# graphql_app = GraphQLRouter(schema, context_getter=get_context)

# app.include_router(graphql_app, prefix="/gql")

# from doc import attachVoyager

# attachVoyager(app, path="/gql/doc")

# print("All initialization is done")


# @app.get("/hello")
# def hello(request: Request):
#     headers = request.headers
#     auth = request.auth
#     user = request.scope["user"]
#     return {"hello": "world", "headers": {**headers}, "auth": f"{auth}", "user": user}


from typing import Any, List
import logging
import os
from pydantic import BaseModel


## AUTO LOAD ENV FILE WITHOUT ADDING COMMANDS
from dotenv import load_dotenv
load_dotenv("environment.txt")



import logging
import logging.handlers
import socket
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s.%(msecs)03d\t%(levelname)s:\t%(message)s', 
    datefmt='%Y-%m-%dT%I:%M:%S')
SYSLOGHOST = os.getenv("SYSLOGHOST", None)
if SYSLOGHOST is not None:
    [address, strport, *_] = SYSLOGHOST.split(':')
    assert len(_) == 0, f"SYSLOGHOST {SYSLOGHOST} has unexpected structure, try `localhost:514` or similar (514 is UDP port)"
    port = int(strport)
    my_logger = logging.getLogger()
    my_logger.setLevel(logging.INFO)
    handler = logging.handlers.SysLogHandler(address=(address, port), socktype=socket.SOCK_DGRAM)
    #handler = logging.handlers.SocketHandler('10.10.11.11', 611)
    my_logger.addHandler(handler)



from fastapi import FastAPI, Request, Depends
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager

from DBDefinitions import ComposeConnectionString

## Zabezpecuje prvotni inicializaci DB a definovani Nahodne struktury pro "Univerzity"
# from gql_workflow.DBFeeder import createSystemDataStructureRoleTypes, createSystemDataStructureGroupTypes

connectionString = ComposeConnectionString()

appcontext = {}
@asynccontextmanager
async def initEngine(app: FastAPI):

    from DBDefinitions import startEngine, ComposeConnectionString

    connectionstring = ComposeConnectionString()
    makeDrop = os.getenv("DEMO", None) == "True"
    asyncSessionMaker = await startEngine(
        connectionstring=connectionstring,
        makeDrop=makeDrop,
        makeUp=True
    )

    appcontext["asyncSessionMaker"] = asyncSessionMaker

    logging.info("engine started")

    from utils.DBFeeder import initDB
    await initDB(asyncSessionMaker)

    logging.info("data (if any) imported")
    yield


from GraphTypeDefinitions import schema
from utils.sentinel import sentinel

async def get_context(request: Request):
    asyncSessionMaker = appcontext.get("asyncSessionMaker", None)
    if asyncSessionMaker is None:
        async with initEngine(app) as cntx:
            pass
        
    from utils.Dataloaders import createLoadersContext, createUgConnectionContext
    context = createLoadersContext(appcontext["asyncSessionMaker"])
    i = Item(query = "")
    # i.query = ""
    # i.variables = {}
    logging.info(f"before sentinel current user is {request.scope.get('user', None)}")
    await sentinel(request, i)
    logging.info(f"after sentinel current user is {request.scope.get('user', None)}")
    connectionContext = createUgConnectionContext(request=request)
    result = {**context, **connectionContext}
    result["request"] = request
    result["user"] = request.scope.get("user", None)
    logging.info(f"context created {result}")
    return result

app = FastAPI(lifespan=initEngine)

from doc import attachVoyager
attachVoyager(app, path="/gql/doc")

print("All initialization is done")
@app.get('/hello')
def hello(request: Request):
    headers = request.headers
    auth = request.auth
    user = request.scope["user"]
    return {'hello': 'world', 'headers': {**headers}, 'auth': f"{auth}", 'user': user}


graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)

class Item(BaseModel):
    query: str
    variables: dict = {}
    operationName: str = None

app.include_router(graphql_app, prefix="/gql2")

@app.get("/gql")
async def graphiql(request: Request):
    return await graphql_app.render_graphql_ide(request)

from utils.sentinel import sentinel

@app.post("/gql")
async def apollo_gql(request: Request, item: Item):
    DEMOE = os.getenv("DEMO", None)
    # logging.info(f"apollo_gql DEMO {DEMOE} {type(DEMOE)}, {DEMO}")
    logging.info(f"asking sentinel for advice (is user authenticated?)")
    sentinelResult = await sentinel(request, item)
    if DEMOE == "False":
        if sentinelResult:
            return sentinelResult
        logging.info(f"sentinel test passed for user {request.scope['user']}")
    else:
        request.scope["user"] = {"id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"}
        logging.info(f"sentinel skippend because of DEMO mode")
    try:
        context = await get_context(request)
        logging.info(f"executing \n {item.query} \n with \n {item.variables}")
        schemaresult = await schema.execute(query=item.query, variable_values=item.variables, operation_name=item.operationName, context_value=context)
        # schemaresult = await schema.execute(query=item.query, variable_values=item.variables, context_value=context)
        # assert 1 == 0, ":)"
    except Exception as e:
        logging.info(f"error during schema execute {e}")
        return {"data": None, "errors": [f"{type(e).__name__}: {e}"]}
    
    logging.info(f"schema execute result \n{schemaresult}")
    result = {"data": schemaresult.data}
    if schemaresult.errors:
        result["errors"] = [f"{error}" for error in schemaresult.errors]
    return result

# from uoishelpers.authenticationMiddleware import BasicAuthenticationMiddleware302, BasicAuthBackend
# app.add_middleware(BasicAuthenticationMiddleware302, backend=BasicAuthBackend(
#         JWTPUBLICKEY = JWTPUBLICKEY,
#         JWTRESOLVEUSERPATH = JWTRESOLVEUSERPATH
# ))

import os
os.environ["DEMO"] = "True"
DEMO = os.getenv("DEMO", None)
assert DEMO is not None, "DEMO environment variable must be explicitly defined"
assert (DEMO == "True") or (DEMO == "False"), "DEMO environment variable can have only `True` or `False` values"
DEMO = DEMO == "True"

if DEMO:
    print("####################################################")
    print("#                                                  #")
    print("# RUNNING IN DEMO                                  #")
    print("#                                                  #")
    print("####################################################")

    logging.info("####################################################")
    logging.info("#                                                  #")
    logging.info("# RUNNING IN DEMO                                  #")
    logging.info("#                                                  #")
    logging.info("####################################################")

if not DEMO:
    GQLUG_ENDPOINT_URL = os.getenv("GQLUG_ENDPOINT_URL", None)
    assert GQLUG_ENDPOINT_URL is not None, "GQLUG_ENDPOINT_URL environment variable must be explicitly defined"
    JWTPUBLICKEYURL = os.getenv("JWTPUBLICKEYURL", None)
    assert JWTPUBLICKEYURL is not None, "JWTPUBLICKEYURL environment variable must be explicitly defined"
    JWTRESOLVEUSERPATHURL = os.getenv("JWTRESOLVEUSERPATHURL", None)
    assert JWTRESOLVEUSERPATHURL is not None, "JWTRESOLVEUSERPATHURL environment variable must be explicitly defined"