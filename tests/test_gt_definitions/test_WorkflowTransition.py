import sqlalchemy
import asyncio
import pytest

# from ..uoishelpers.uuid import UUIDColumn

from GraphTypeDefinitions import schema


from tests.gqlshared import (
    createByIdTest,
    createPageTest,
    createResolveReferenceTest,
    createFrontendQuery,
    createUpdateQuery,
)

###     Query test


test_reference_workflowtransition = createResolveReferenceTest(
    tableName="awworkflowtransitions", gqltype="WorkflowTransitionGQLModel", attributeNames=["id"]
)

test_query_workflowtransition_by_id = createByIdTest(
    tableName="awworkflowtransitions", queryEndpoint="workflowTransitionById", attributeNames=["id"]
)

test_query_workflowtransition = createPageTest(
    tableName="awworkflowtransitions", queryEndpoint="workflowTransition", attributeNames=["id"]
)
