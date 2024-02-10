# import pytest
# import sqlalchemy
# import sys
# import asyncio
# import os

# from DBDefinitions import startEngine, ComposeConnectionString


# from DBDefinitions import (
#     BaseModel,
#     AuthorizationModel,
#     AuthorizationUserModel,
#     AuthorizationRoleTypeModel,
#     AuthorizationGroupModel,
#     WorkflowModel,
#     WorkflowStateModel,
#     WorkflowTransitionModel,
#     WorkflowStateUserModel,
#     WorkflowStateRoleTypeModel,
# )

# from .shared import prepare_demodata, prepare_in_memory_sqllite, get_demodata


# @pytest.mark.asyncio
# async def test_load_demo_data():
#     async_session_maker = await prepare_in_memory_sqllite()
#     await prepare_demodata(async_session_maker)
#     # data = get_demodata()


# def test_connection_string():
#     from DBDefinitions import ComposeConnectionString

#     connection_string = ComposeConnectionString()

#     assert "://" in connection_string


# @pytest.mark.asyncio
# async def test_table_start_engine():
#     connection_string = "sqlite+aiosqlite:///:memory:"
#     async_session_maker = await startEngine(
#         connection_string, makeDrop=True, makeUp=True
#     )

#     assert async_session_maker is not None


# from utils.DBFeeder import initDB


# @pytest.mark.asyncio
# async def test_initDB():
#     connection_string = "sqlite+aiosqlite:///:memory:"
#     async_session_maker = await startEngine(
#         connection_string, makeDrop=True, makeUp=True
#     )

#     assert async_session_maker is not None
#     await initDB(async_session_maker)


# # @pytest.fixture
# # def mock_env(monkeypatch):
# #     monkeypatch.setenv("POSTGRES_USER", "testuser")
# #     monkeypatch.setenv("POSTGRES_PASSWORD", "testpass")
# #     monkeypatch.setenv("POSTGRES_DB", "testdb")
# #     monkeypatch.setenv("POSTGRES_HOST", "localhost:5432")


# # @pytest.mark.asyncio
# # async def test_start_engine_create(mock_env):
# #     # Test database creation
# #     async_session_maker = await startEngine(
# #         ComposeConnectionString(), makeDrop=True, makeUp=True
# #     )
# #     assert async_session_maker is not None
# #     # Include additional assertions to validate database state


# # @pytest.mark.asyncio
# # async def test_start_engine_drop(mock_env):
# #     # Test dropping the database
# #     async_session_maker = await startEngine(
# #         ComposeConnectionString(), makeDrop=True, makeUp=False
# #     )
# #     assert async_session_maker is not None
# #     # Include additional assertions to validate database state


# # def test_compose_connection_string(mock_env):
# #     # Test the connection string composition
# #     conn_str = ComposeConnectionString()
# #     expected_str = "postgresql+asyncpg://testuser:testpass@localhost:5432/testdb"
# #     assert conn_str == expected_str


# # Additional tests for error handling and edge cases
