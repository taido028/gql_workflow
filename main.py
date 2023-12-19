from typing import List
import typing

import asyncio

from fastapi import FastAPI, Request
import strawberry
from strawberry.fastapi import GraphQLRouter

## Definice GraphQL typu (pomoci strawberry https://strawberry.rocks/)
## Strawberry zvoleno kvuli moznosti mit federovane GraphQL API (https://strawberry.rocks/docs/guides/federation, https://www.apollographql.com/docs/federation/)

## Definice DB typu (pomoci SQLAlchemy https://www.sqlalchemy.org/)
## SQLAlchemy zvoleno kvuli moznost komunikovat s DB asynchronne
## https://docs.sqlalchemy.org/en/14/core/future.html?highlight=select#sqlalchemy.future.select
from gql_workflow.DBDefinitions import startEngine, ComposeConnectionString

## Zabezpecuje prvotni inicializaci DB a definovani Nahodne struktury pro "Univerzity"
# from gql_workflow.DBFeeder import createSystemDataStructureRoleTypes, createSystemDataStructureGroupTypes
connectionString = ComposeConnectionString()

from strawberry.asgi import GraphQL
from gql_workflow.Dataloaders import createLoaders
import logging

appcontext = {}

from contextlib import asynccontextmanager


@asynccontextmanager
async def initEngine(app: FastAPI):
    from gql_workflow.DBDefinitions import startEngine, ComposeConnectionString

    connectionstring = ComposeConnectionString()

    asyncSessionMaker = await startEngine(
        connectionstring=connectionstring, makeDrop=True, makeUp=True
    )

    appcontext["asyncSessionMaker"] = asyncSessionMaker

    logging.info("engine started")

    from gql_workflow.DBFeeder import initDB

    await initDB(asyncSessionMaker)

    logging.info("data (if any) imported")
    yield


from gql_workflow._GraphTypeDefinitions import schema

app = FastAPI(lifespan=initEngine)


async def get_context():
    asyncSessionMaker = appcontext.get("asyncSessionMaker", None)
    if asyncSessionMaker is None:
        async with initEngine(app) as cntx:
            pass

    from gql_workflow.Dataloaders import createLoadersContext

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
