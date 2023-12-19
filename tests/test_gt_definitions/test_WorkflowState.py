import sqlalchemy
import asyncio
import pytest

# from ..uoishelpers.uuid import UUIDColumn

from GraphTypeDefinitions import schema

from tests.shared import (
    prepare_demodata,
    prepare_in_memory_sqllite,
    get_demodata,
    createContext,
)

from tests.gqlshared import createByIdTest, createPageTest, createResolveReferenceTest


###     Query test

test_reference_workflowstate = createResolveReferenceTest(
    tableName="awworkflowstates", gqltype="WorkflowStateGQLModel"
)
test_query_workflowstate = createPageTest(
    tableName="awworkflowstates", queryEndpoint="workflowState"
)
test_query_workflowstate_by_id = createByIdTest(
    tableName="awworkflowstates", queryEndpoint="workflowStateById"
)
