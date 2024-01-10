import sqlalchemy
import asyncio
import pytest

# from ..uoishelpers.uuid import UUIDColumn




from tests.gqlshared import (
    createByIdTest,
    createPageTest,
    createResolveReferenceTest,
)

###     Query test


test_reference_workflowtransition = createResolveReferenceTest(
    tableName="awworkflowtransitions", gqltype="WorkflowTransitionGQLModel", attributeNames=["id"]
)

test_query_workflowtransition_by_id = createByIdTest(
    tableName="awworkflowtransitions", queryEndpoint="workflowTransitionById", attributeNames=["id", "name"]
)

test_query_workflowtransition = createPageTest(
    tableName="awworkflowtransitions", queryEndpoint="workflowTransition", attributeNames=["id"]
)
