from typing import List, Any
import typing
import os
from pydantic import BaseModel


import asyncio

from fastapi import FastAPI, Request
import strawberry
from strawberry.fastapi import GraphQLRouter

## Definice GraphQL typu (pomoci strawberry https://strawberry.rocks/)
## Strawberry zvoleno kvuli moznosti mit federovane GraphQL API (https://strawberry.rocks/docs/guides/federation, https://www.apollographql.com/docs/federation/)

## Definice DB typu (pomoci SQLAlchemy https://www.sqlalchemy.org/)
## SQLAlchemy zvoleno kvuli moznost komunikovat s DB asynchronne
## https://docs.sqlalchemy.org/en/14/core/future.html?highlight=select#sqlalchemy.future.select
from DBDefinitions import startEngine, ComposeConnectionString

## Zabezpecuje prvotni inicializaci DB a definovani Nahodne struktury pro "Univerzity"
# from gql_workflow.DBFeeder import createSystemDataStructureRoleTypes, createSystemDataStructureGroupTypes
connectionString = ComposeConnectionString()

from strawberry.asgi import GraphQL
from utils.Dataloaders import createLoaders
import logging

appcontext = {}

from contextlib import asynccontextmanager


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

app = FastAPI(lifespan=initEngine)



# class Item(BaseModel):
#     query: str
#     variables: dict = {}
#     operationName: str = None


# async def get_context(request: Request):
#     asyncSessionMaker = appcontext.get("asyncSessionMaker", None)
#     if asyncSessionMaker is None:
#         async with initEngine(app) as cntx:
#             pass
        
#     from utils.Dataloaders import createLoadersContext, createUgConnectionContext
#     context = createLoadersContext(appcontext["asyncSessionMaker"])
#     i = Item(query = "")
#     # i.query = ""
#     # i.variables = {}
#     logging.info(f"before sentinel current user is {request.scope.get('user', None)}")
#     await sentinel(request, i)
#     logging.info(f"after sentinel current user is {request.scope.get('user', None)}")
#     connectionContext = createUgConnectionContext(request=request)
#     result = {**context, **connectionContext}
#     result["request"] = request
#     result["user"] = request.scope.get("user", None)
#     logging.info(f"context created {result}")
#     return result



async def get_context():
    asyncSessionMaker = appcontext.get("asyncSessionMaker", None)
    if asyncSessionMaker is None:
        async with initEngine(app) as cntx:
            pass

    from utils.Dataloaders import createLoadersContext

    context = createLoadersContext(appcontext["asyncSessionMaker"])
    return context



graphql_app = GraphQLRouter(schema, context_getter=get_context)

app.include_router(graphql_app, prefix="/gql")

from doc import attachVoyager

attachVoyager(app, path="/gql/doc")

print("All initialization is done")


@app.get("/hello")
def hello(request: Request):
    headers = request.headers
    auth = request.auth
    user = request.scope["user"]
    return {"hello": "world", "headers": {**headers}, "auth": f"{auth}", "user": user}
