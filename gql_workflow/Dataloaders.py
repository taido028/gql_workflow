from uoishelpers.dataloaders import createIdLoader, createFkeyLoader

from functools import cache

from gql_workflow.DBDefinitions import (
    WorkflowModel,
    WorkflowStateModel,
    WorkflowStateRoleTypeModel,
    WorkflowStateUserModel,
    WorkflowTransitionModel,
    AuthorizationGroupModel,
    AuthorizationModel,
    AuthorizationRoleTypeModel,
    AuthorizationUserModel,
)

dbmodels = {
    "workflows": WorkflowModel,
    "workflowstates": WorkflowStateModel,
    "workflowstateroletypes": WorkflowStateRoleTypeModel,
    "workflowstateusers": WorkflowStateUserModel,
    "workflowtransitions": WorkflowTransitionModel,
    "authorizationgroups": AuthorizationGroupModel,
    "authorizations": AuthorizationModel,
    "authorizationroletypes": AuthorizationRoleTypeModel,
    "authorizationusers": AuthorizationUserModel,
}


class Loaders:
    # authorizations = None
    # authorizationgroups = None
    # authorizationroletypes = None
    # authorizationusers = None
    workflows = None
    workflowstates = None
    workflowstateroletypes = None
    workflowstateusers = None
    workflowtransitions = None

    pass


def createLoaders(asyncSessionMaker, models=dbmodels) -> Loaders:
    class Loaders:
        @property
        @cache
        def workflows(self):
            return createIdLoader(asyncSessionMaker, models["workflows"])

        @property
        @cache
        def workflowstates(self):
            return createIdLoader(asyncSessionMaker, models["workflowstates"])

        @property
        @cache
        def workflowstateroletypes(self):
            return createIdLoader(asyncSessionMaker, models["workflowstateroletypes"])

        @property
        @cache
        def workflowstateusers(self):
            return createIdLoader(asyncSessionMaker, models["workflowstateusers"])

        @property
        @cache
        def workflowtransitions(self):
            return createIdLoader(asyncSessionMaker, models["workflowtransitions"])

        """
        def createLambda(loaderName, DBModel):
            return lambda self: createIdLoader(asyncSessionMaker, DBModel)

        attrs = {}
        for key, DBModel in models.items():
            attrs[key] = property(cache(createLambda(key, DBModel)))

        Loaders = type('Loaders', (), attrs)   
        return Loaders()
        """

    return Loaders()


def createLoadersContext(asyncSessionMaker):
    return {"loaders": createLoaders(asyncSessionMaker)}
