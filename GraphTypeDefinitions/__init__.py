from typing import List, Union
import typing
import strawberry
import uuid
from contextlib import asynccontextmanager


from .externals import UserGQLModel
from ._GraphPermissions import RoleBasedPermission
from utils.Dataloaders import getUserFromInfo

####################################################################################################################


@strawberry.type(description="""Type for query root""")
class Query:
    # from .authorizationGQLModel import authorization_by_id

    # authorization_by_id = authorization_by_id

    # from .authorizationGQLModel import authorization_page

    # authorization_page = authorization_page

    # from .authorizationGroupGQLModel import authorization_group_by_id

    # authorization_group_by_id = authorization_group_by_id

    # from .authorizationGroupGQLModel import authorization_group_page

    # authorization_group_page = authorization_group_page

    from .workflowGQLModel import workflow_by_id

    workflow_by_id = workflow_by_id

    from .workflowGQLModel import workflow_page

    workflow_page = workflow_page

    from .workflowStateGQLModel import workflow_state

    workflow_state = workflow_state

    from .workflowStateGQLModel import workflow_state_by_id

    workflow_state_by_id = workflow_state_by_id

    from .workflowStateRoleTypeGQLModel import workflow_state_role_type

    workflow_state_role_type = workflow_state_role_type

    from .workflowStateRoleTypeGQLModel import workflow_state_role_type_by_id

    workflow_state_role_type_by_id = workflow_state_role_type_by_id

    from .workflowStateUserGQLModel import workflow_state_user

    workflow_state_user = workflow_state_user

    from .workflowStateUserGQLModel import workflow_state_user_by_id

    workflow_state_user_by_id = workflow_state_user_by_id

    from .workflowTransitionGQLModel import workflow_transition

    workflow_transition = workflow_transition

    from .workflowTransitionGQLModel import workflow_transition_by_id

    workflow_transition_by_id = workflow_transition_by_id


######################################################################################################################
#
#
# Mutations
#
#
######################################################################################################################


@strawberry.type(description="""Root mutation type""")
class Mutation:
    # from .authorizationGQLModel import authorization_insert
    # authorization_insert = authorization_insert

    # from .authorizationGroupGQLModel import authorization_add_group
    # authorization_add_group = authorization_add_group

    # from .authorizationGroupGQLModel import authorization_remove_group
    # authorization_remove_group = authorization_remove_group

    # from .authorizationRoleTypeGQLModel import authorization_add_role
    # authorization_add_role = authorization_add_role

    # from .authorizationRoleTypeGQLModel import authorization_remove_role
    # authorization_remove_role = authorization_remove_role

    # from .authorizationUserGQLModel import authorization_add_user
    # authorization_add_user = authorization_add_user

    # from .authorizationUserGQLModel import authorization_remove_user
    # authorization_remove_user = authorization_remove_user

    from .workflowGQLModel import workflow_insert

    workflow_insert = workflow_insert

    from .workflowGQLModel import workflow_update

    workflow_update = workflow_update

    from .workflowStateGQLModel import workflow_state_insert

    workflow_state_insert = workflow_state_insert

    from .workflowStateGQLModel import workflow_state_update

    workflow_state_update = workflow_state_update

    # from .WorkflowStateRoleTypeGQLModel import *

    from .workflowTransitionGQLModel import workflow_transition_insert

    workflow_transition_insert = workflow_transition_insert

    from .workflowTransitionGQLModel import workflow_transition_update

    workflow_transition_update = workflow_transition_update

    # from .WorkflowStateUserGQLModel import *
    from .workflowStateUserGQLModel import workflow_state_add_user

    workflow_state_add_user = workflow_state_add_user

    from .workflowStateUserGQLModel import workflow_state_remove_user

    workflow_state_remove_user = workflow_state_remove_user

    from .workflowStateRoleTypeGQLModel import workflow_state_add_role

    workflow_state_add_role = workflow_state_add_role

    from .workflowStateRoleTypeGQLModel import workflow_state_remove_role

    workflow_state_remove_role = workflow_state_remove_role


schema = strawberry.federation.Schema(Query, types=(UserGQLModel,), mutation=Mutation)
