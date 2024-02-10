import os
from unittest.mock import patch
from DBDefinitions import ComposeConnectionString


import pytest
import sqlalchemy
from unittest.mock import AsyncMock, patch
from DBDefinitions import startEngine, BaseModel  # Replace 'your_module' with actual module name


@pytest.mark.asyncio
async def test_table_start_engine():
    connection_string = "sqlite+aiosqlite:///:memory:"
    async_session_maker = await startEngine(
        connection_string, makeDrop=True, makeUp=True
    )

    assert async_session_maker is not None


from utils.DBFeeder import initDB


@pytest.mark.asyncio
async def test_initDB():
    connection_string = "sqlite+aiosqlite:///:memory:"
    async_session_maker = await startEngine(
        connection_string, makeDrop=True, makeUp=True
    )

    assert async_session_maker is not None
    await initDB(async_session_maker)



def test_compose_connection_string_default_values():
    with patch.dict(os.environ, {}, clear=True):
        conn_string = ComposeConnectionString()
        assert conn_string == "postgresql+asyncpg://postgres:example@localhost:5432/data"


def test_compose_connection_string_custom_values():
    custom_env = {
        "POSTGRES_USER": "custom_user",
        "POSTGRES_PASSWORD": "custom_password",
        "POSTGRES_DB": "custom_db",
        "POSTGRES_HOST": "custom_host:1234"
    }
    with patch.dict(os.environ, custom_env, clear=True):
        conn_string = ComposeConnectionString()
        assert conn_string == "postgresql+asyncpg://custom_user:custom_password@custom_host:1234/custom_db"