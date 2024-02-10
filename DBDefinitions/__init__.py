import sqlalchemy


from .Base import BaseModel
from .uuid import UUIDColumn

from .AuthorizationGroupModel import AuthorizationGroupModel
from .AuthorizationModel import AuthorizationModel
from .AuthorizationRoleTypeModel import AuthorizationRoleTypeModel
from .AuthorizationUserModel import AuthorizationUserModel
from .WorkflowModel import WorkflowModel
from .WorkflowStateModel import WorkflowStateModel
from .WorkflowStateRoleTypeModel import WorkflowStateRoleTypeModel
from .WorkflowStateUserModel import WorkflowStateUserModel
from .WorkflowTransitionModel import WorkflowTransitionModel


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine


async def startEngine(connectionstring, makeDrop=False, makeUp=True):
    """Provede nezbytne ukony a vrati asynchronni SessionMaker"""
    asyncEngine = create_async_engine(connectionstring, pool_pre_ping=True)
    # pool_size=20, max_overflow=10, pool_recycle=60) #pool_pre_ping=True, pool_recycle=3600

    async with asyncEngine.begin() as conn:
        if makeDrop:
            await conn.run_sync(BaseModel.metadata.drop_all)
            print("BaseModel.metadata.drop_all finished")
        if makeUp:
            try: await conn.run_sync(BaseModel.metadata.create_all); print("BaseModel.metadata.create_all finished")
            except sqlalchemy.exc.NoReferencedTableError as e: print(e, "\nUnable to automatically create tables")

    async_sessionMaker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )
    return async_sessionMaker


import os


def ComposeConnectionString():
    """Odvozuje connectionString z promennych prostredi (nebo z Docker Envs, coz je fakticky totez).
    Lze predelat na napr. konfiguracni file.
    """
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "example")
    database = os.environ.get("POSTGRES_DB", "data")
    hostWithPort = os.environ.get("POSTGRES_HOST", "localhost:5432")

    driver = "postgresql+asyncpg"  # "postgresql+psycopg2"
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"

    return connectionstring
