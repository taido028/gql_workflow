import sqlalchemy
import asyncio
import pytest

# from ..uoishelpers.uuid import UUIDColumn

from gql_workflow.GraphTypeDefinitions import schema

from tests.shared import (
    prepare_demodata,
    prepare_in_memory_sqllite,
    get_demodata,
    createContext,
)

from tests.gqlshared import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest
)


###     Query test


test_reference_workflowstateuser = createResolveReferenceTest(tableName="awworkflowstateusers", gqltype="WorkflowStateUserGQLModel")
test_query_workflowstateuser= createPageTest(tableName="awworkflowstateusers", queryEndpoint="workflowStateUser")
test_query_workflowstateuser_by_id= createByIdTest(tableName="awworkflowstateusers", queryEndpoint="workflowStateUserById")