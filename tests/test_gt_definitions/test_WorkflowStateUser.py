import sqlalchemy
import asyncio
import pytest

# from ..uoishelpers.uuid import UUIDColumn


from tests.gqlshared import(
    createByIdTest,
    createPageTest,
    createResolveReferenceTest)


###     Query test


test_reference_workflowstateuser = createResolveReferenceTest(
    tableName="awworkflowstateusers", gqltype="WorkflowStateUserGQLModel"
)
test_query_workflowstateuser = createPageTest(
    tableName="awworkflowstateusers", queryEndpoint="workflowStateUser", attributeNames=["id"]
)
test_query_workflowstateuser_by_id = createByIdTest(
    tableName="awworkflowstateusers", queryEndpoint="workflowStateUserById", attributeNames=["id"]
)
