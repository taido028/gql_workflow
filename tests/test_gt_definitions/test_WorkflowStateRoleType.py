import sqlalchemy
import asyncio
import pytest

# from ..uoishelpers.uuid import UUIDColumn


from tests.shared import (
    prepare_demodata,
    prepare_in_memory_sqllite,
    get_demodata,
)

from tests.gqlshared import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest
    )


###     Query test


test_reference_workflowstateroletype = createResolveReferenceTest(
    tableName="awworkflowstateroletypes", gqltype="WorkflowStateRoleTypeGQLModel"
)
test_query_workflowstateroletype = createPageTest(
    tableName="awworkflowstateroletypes", queryEndpoint="workflowStateRoleType"
)
test_query_workflowstateroletype_by_id = createByIdTest(
    tableName="awworkflowstateroletypes", queryEndpoint="workflowStateRoleTypeById"
)
