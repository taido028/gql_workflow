import logging
import sqlalchemy
import uuid
import sys
import asyncio
import json
import pytest
import re

from GraphTypeDefinitions import schema

from .shared import (
    prepare_demodata,
    prepare_in_memory_sqllite,
    get_demodata,
    CreateContext,
    CreateSchemaFunction,
)
from .client import CreateClientFunction


def append(queryname="queryname", query=None, mutation=None, variables={}):
    with open("./queries.txt", "a", encoding="utf-8") as file:
        if (query is not None) and ("mutation" in query):
            jsonData = {"query": None, "mutation": query, "variables": variables}
        else:
            jsonData = {"query": query, "mutation": mutation, "variables": variables}
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


###     Query test

# This is the general function for all ById test.


def createByIdTest(tableName, queryEndpoint, attributeNames=["id", "name"]):
    @pytest.mark.asyncio
    async def result_test():
        def test_result(response):
            print("response", response)
            errors = response.get("errors", None)
            assert errors is None

            response_data = response.get("data", None)
            assert response_data is not None

            response_data = response_data[queryEndpoint]
            assert response_data is not None

            for attribute in attributeNames:
                assert response_data[attribute] == f"{data_row[attribute]}"

        schema_executor = CreateSchemaFunction()
        _, client_executor = CreateClientFunction()

        data = get_demodata()
        data_row = data[tableName][0]
        content = "{" + ", ".join(attributeNames) + "}"
        query = "query($id: UUID!){" f"{queryEndpoint}(id: $id)" f"{content}" "}"

        variable_values = {"id": f'{data_row["id"]}'}

        append(
            queryname=f"{queryEndpoint}_{tableName}",
            query=query,
            variables=variable_values,
        )
        logging.debug(f"query {query} with {variable_values}")

        response = await schema_executor(query, variable_values)
        test_result(response)
        response = await client_executor(query, variable_values)
        test_result(response)

    return result_test


# This is the general function for all page test.


def createPageTest(tableName, queryEndpoint, attributeNames=["id"]):
    @pytest.mark.asyncio
    async def result_test() -> None:
        def test_result(response) -> None:
            print("response", response)
            errors = response.get("errors", None)
            assert errors is None

            response_data = response.get("data", None)
            assert response_data is not None

            response_data = response_data.get(queryEndpoint, None)
            assert response_data is not None
            data_rows = data[tableName]

            for row_a, row_b in zip(response_data, data_rows):
                for attribute in attributeNames:
                    assert row_a[attribute] == f"{row_b[attribute]}"

        schema_executor = CreateSchemaFunction()
        _, client_executor = CreateClientFunction()

        data = get_demodata()

        content = "{" + ", ".join(attributeNames) + "}"
        query = "query{ " f"{queryEndpoint} {content}" "}"

        append(queryname=f"{queryEndpoint}_{tableName}", query=query)

        response = await schema_executor(query)
        test_result(response)
        response = await client_executor(query)
        test_result(response)

    return result_test


# This is the general function for all Resolve test.


def createResolveReferenceTest(tableName: str, gqltype: str, attributeNames=["id"]):
    @pytest.mark.asyncio
    async def result_test():
        def test_result(resp):
            print("response", resp)
            errors = resp.get("errors", None)
            assert errors is None

            response_data = resp.get("data", None)
            assert response_data is not None

            logging.info(f"response_data: {response_data}")
            response_data = response_data.get("_entities", None)
            assert response_data is not None

            assert len(response_data) == 1
            response_data = response_data[0]

            assert response_data["id"] == row_id

        schema_executor = CreateSchemaFunction()
        _, client_executor = CreateClientFunction()

        content = "{" + ", ".join(attributeNames) + "}"

        data = get_demodata()
        table = data[tableName]
        for row in table:
            row_id = f"{row['id']}"

            query = (
                "query($rep: [_Any!]!)"
                + "{"
                + "_entities(representations: $rep)"
                + "{"
                + f"    ...on {gqltype} {content}"
                + "}"
                + "}"
            )

            variable_values = {"rep": [{"__typename": f"{gqltype}", "id": f"{row_id}"}]}

            logging.info(f"query representation: {query} with {variable_values}")
            response = await client_executor(query, {**variable_values})
            test_result(response)
            response = await schema_executor(query, {**variable_values})
            test_result(response)

        append(queryname=f"{gqltype}_representation", query=query)

    return result_test


###     Mutation test

# This is the general function for insert mutation test.


def createFrontendQuery(query="{}", variables={}, asserts=[]):
    @pytest.mark.asyncio
    async def test_frontend_query() -> None:
        logging.debug("createFrontendQuery")
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)
        context_value = CreateContext(async_session_maker)
        logging.debug(f"query for {query} with {variables}")
        print(f"query for {query} with {variables}")

        append(queryname=f"query", query=query, variables=variables)

        resp = await schema.execute(
            query=query, variable_values=variables, context_value=context_value
        )

        assert resp.errors is None
        respdata = resp.data
        logging.debug(f"response: {respdata}")
        for a in asserts:
            a(respdata)

    return test_frontend_query


# This is general function for update test.


def createUpdateQuery(query="{}", variables={}, tableName=""):
    @pytest.mark.asyncio
    async def test_update() -> None:
        logging.debug("test_update")
        assert variables.get("id", None) is not None, "variables has not id"
        variables["id"] = uuid.UUID(f"{variables['id']}")
        assert (
            "$lastchange: DateTime!" in query
        ), "query must have parameter $lastchange: DateTime!"
        assert (
            "lastchange: $lastchange" in query
        ), "query must use lastchange: $lastchange"
        assert tableName != "", "missing table name"

        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        print("variables['id']", variables, flush=True)
        statement = sqlalchemy.text(
            f"SELECT id, lastchange FROM {tableName} WHERE id=:id"
        ).bindparams(id=variables["id"])
        # statement = sqlalchemy.text(f"SELECT id, lastchange FROM {tableName}")
        print("statement", statement, flush=True)
        async with async_session_maker() as session:
            rows = await session.execute(statement)
            row = rows.first()

            print("row", row)
            id = row[0]
            lastchange = row[1]

            print(id, lastchange)

        variables["lastchange"] = lastchange
        variables["id"] = f'{variables["id"]}'
        context_value = CreateContext(async_session_maker)
        logging.debug(f"query for {query} with {variables}")
        print(f"query for {query} with {variables}")

        append(queryname=f"query_{tableName}", mutation=query, variables=variables)

        resp = await schema.execute(
            query=query, variable_values=variables, context_value=context_value
        )

        assert resp.errors is None
        respdata = resp.data
        assert respdata is not None
        print("respdata", respdata)
        keys = list(respdata.keys())
        assert len(keys) == 1, "expected update test has one result"
        key = keys[0]
        result = respdata.get(key, None)
        assert result is not None, f"{key} is None (test update) with {query}"
        entity = None
        for key, value in result.items():
            print(key, value, type(value))
            if isinstance(value, dict):
                entity = value
                break
        assert entity is not None, f"expected entity in response to {query}"

        for key, value in entity.items():
            if key in ["id", "lastchange"]:
                continue
            print(
                "attribute check", type(key), f"[{key}] is {value} ?= {variables[key]}"
            )
            assert (
                value == variables[key]
            ), f"test on update failed {value} != {variables[key]}"

    return test_update
