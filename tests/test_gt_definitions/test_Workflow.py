import sqlalchemy
import asyncio
import pytest

# from ..uoishelpers.uuid import UUIDColumn

from gql_workflow.GraphTypeDefinitions import schema


from tests.gqlshared import (
    createByIdTest,
    createPageTest,
    createResolveReferenceTest,
    createFrontendQuery,
    createUpdateQuery,
)

###     Query test


test_reference_workflow = createResolveReferenceTest(
    tableName="awworkflows", gqltype="WorkflowGQLModel"
)
test_query_workflow_page = createPageTest(
    tableName="awworkflows", queryEndpoint="workflowPage", attributeNames=["id"]
)
test_query_workflow_by_id = createByIdTest(
    tableName="awworkflows", queryEndpoint="workflowById", attributeNames=["id"]
)


###     Mutation test


test_insert_workflow = createFrontendQuery(
    query="""mutation($name: string!) {
        result: workflowInsert(workflow: {name: $string}) {
            name
            msg
        }
    }""",
    variables={"name": "another workflow"},
    asserts=[],
)
