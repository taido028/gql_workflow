from uoishelpers.dataloaders import createIdLoader, createFkeyLoader
import logging
from functools import cache

from DBDefinitions import (
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


import asyncio
import os
from aiodataloader import DataLoader
from uoishelpers.resolvers import select, update, delete


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


def getLoadersFromInfo(info) -> Loaders:
    context = info.context
    loaders = context["loaders"]
    return loaders


demouser = {
    "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
    "name": "John",
    "surname": "Newbie",
    "email": "john.newbie@world.com",
    "roles": [
        {
            "valid": True,
            "group": {"id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003", "name": "Uni"},
            "roletype": {
                "id": "ced46aa4-3217-4fc1-b79d-f6be7d21c6b6",
                "name": "administrátor",
            },
        },
        {
            "valid": True,
            "group": {"id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003", "name": "Uni"},
            "roletype": {
                "id": "ae3f0d74-6159-11ed-b753-0242ac120003",
                "name": "rektor",
            },
        },
    ],
}


def getUserFromInfo(info) -> dict | None:
    context = info.context
    # print(list(context.keys()))
    result = context.get("user", None)
    """
    if result is None:
        authorization = context["request"].headers.get("Authorization", None)
        if authorization is not None:
            if "Bearer " in authorization:
                token = authorization.split(" ")[1]
                if token == "2d9dc5ca-a4a2-11ed-b9df-0242ac120003":
                    result = demouser
                    context["user"] = result
    logging.debug("getUserFromInfo", result)
    """
    return result


def getGroupFromInfo(info):
    # Len pre testovacie účely
    result = demouser
    return result
    """
    context = info.context
    # print(list(context.keys()))
    result = context.get("user", None)
    if result is None:
        authorization = context["request"].headers.get("Authorization", None)
        if authorization is not None:
            if 'Bearer ' in authorization:
                token = authorization.split(' ')[1]
                if token == "2d9dc5ca-a4a2-11ed-b9df-0242ac120003":
                    result = demouser
                    context["user"] = result
    logging.debug("getUserFromInfo", result)
    return result
    """


def createLoadersContext(asyncSessionMaker):
    return {"loaders": createLoaders(asyncSessionMaker)}
