import strawberry


@strawberry.type(description="""Type for query root""")
class Query:
    from .authorizationGQLModel import authorization_by_id

    authorization_by_id = authorization_by_id

    from .authorizationGQLModel import authorization_page

    authorization_page = authorization_page

    from .authorizationGroupGQLModel import authorization_group_by_id

    authorization_group_by_id = authorization_group_by_id

    from .authorizationGroupGQLModel import authorization_group_page

    authorization_group_page = authorization_group_page

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
