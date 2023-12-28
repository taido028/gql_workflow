import sqlalchemy
import asyncio
import pytest

# from ..uoishelpers.uuid import UUIDColumn




from tests.gqlshared import( 
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest)


###     Query test

test_reference_workflowstate = createResolveReferenceTest(
    tableName="awworkflowstates", gqltype="WorkflowStateGQLModel"
)
test_query_workflowstate = createPageTest(
    tableName="awworkflowstates", queryEndpoint="workflowState", attributeNames=["id"]
)
test_query_workflowstate_by_id = createByIdTest(
    tableName="awworkflowstates", queryEndpoint="workflowStateById", attributeNames=["id"]
)
