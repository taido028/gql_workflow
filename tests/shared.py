import sqlalchemy
import sys
import asyncio

# setting path
sys.path.append("../gql_workflow")

import pytest
import logging

# from ..uoishelpers.uuid import UUIDColumn
from DBDefinitions import (
    BaseModel,
    AuthorizationModel,
    AuthorizationUserModel,
    AuthorizationRoleTypeModel,
    AuthorizationGroupModel,
    WorkflowModel,
    WorkflowStateModel,
    WorkflowTransitionModel,
    WorkflowStateUserModel,
    WorkflowStateRoleTypeModel,
)


from GraphTypeDefinitions import schema


async def prepare_in_memory_sqllite():
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker

    asyncEngine = create_async_engine("sqlite+aiosqlite:///:memory:")
    # asyncEngine = create_async_engine("sqlite+aiosqlite:///data.sqlite")
    async with asyncEngine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async_session_maker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session_maker


from utils.DBFeeder import get_demodata


async def prepare_demodata(async_session_maker):
    data = get_demodata()

    print(data["awworkflows"])
    print(type(data["awworkflows"][0]["id"]))
    from uoishelpers.feeders import ImportModels

    await ImportModels(
        async_session_maker,
        [
            # AuthorizationModel,
            # AuthorizationGroupModel,
            # AuthorizationUserModel,
            # AuthorizationRoleTypeModel,
            WorkflowModel,
            WorkflowStateModel,
            WorkflowStateRoleTypeModel,
            WorkflowStateUserModel,
        ],
        data,
    )


from utils.Dataloaders import createLoadersContext


# async def createContext(asyncSessionMaker):
#     return {
#         "asyncSessionMaker": asyncSessionMaker,
#         "all": await createLoaders(asyncSessionMaker),
#     }


def CreateContext(async_session_maker, with_user=True):
    loaders_context = createLoadersContext(async_session_maker)
    user = {
        "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
        "name": "John",
        "surname": "Newbie",
        "email": "john.newbie@world.com",
    }
    if with_user:
        loaders_context["user"] = user

    return loaders_context


def create_info(async_session_maker, with_user=True):
    class Request:
        @property
        def headers(self):
            return {"Authorization": "Bearer 2d9dc5ca-a4a2-11ed-b9df-0242ac120003"}

    class Info:
        @property
        def context(self):
            context = CreateContext(async_session_maker, with_user=with_user)
            context["request"] = Request()
            return context

    return Info()


def CreateSchemaFunction():
    async def result(query, variables={}):
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)
        context_value = createLoadersContext(async_session_maker)
        logging.debug(f"query for {query} with {variables}")
        print(f"query for {query} with {variables}")
        resp = await schema.execute(
            query=query, variable_values=variables, context_value=context_value
        )

        assert resp.errors is None
        respdata = resp.data
        logging.debug(f"response: {respdata}")

        result = {"data": respdata, "errors": resp.errors}
        return result

    return result
