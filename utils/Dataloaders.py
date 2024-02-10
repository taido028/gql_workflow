from uoishelpers.dataloaders import createIdLoader, createFkeyLoader
import logging
from functools import cache

from DBDefinitions import (
    WorkflowModel,
    WorkflowStateModel,
    WorkflowStateRoleTypeModel,
    WorkflowStateUserModel,
    WorkflowTransitionModel,
    # AuthorizationGroupModel,
    # AuthorizationModel,
    # AuthorizationRoleTypeModel,
    # AuthorizationUserModel,
)

dbmodels = {
    "workflows": WorkflowModel,
    "workflowstates": WorkflowStateModel,
    "workflowstateroletypes": WorkflowStateRoleTypeModel,
    "workflowstateusers": WorkflowStateUserModel,
    "workflowtransitions": WorkflowTransitionModel,
    # "authorizationgroups": AuthorizationGroupModel,
    # "authorizations": AuthorizationModel,
    # "authorizationroletypes": AuthorizationRoleTypeModel,
    # "authorizationusers": AuthorizationUserModel,
}

import datetime
import aiohttp
import asyncio
import os
from aiodataloader import DataLoader
from uoishelpers.resolvers import select, update, delete
from uoishelpers.dataloaders import createIdLoader


@cache
def composeAuthUrl():
    hostname = os.environ.get("GQLUG_ENDPOINT_URL", None)
    assert hostname is not None, "undefined GQLUG_ENDPOINT_URL"
    assert "://" in hostname, "probably bad formated url, has it 'protocol' part?"
    assert "." not in hostname, "security check failed, change source code"
    return hostname

###

class AuthorizationLoader(DataLoader):

    query = """query($id: UUID!){result: rbacById(id: $id) {roles {user { id } group { id } roletype { id }}}}"""
            # variables = {"id": rbacobject}

    roleUrlEndpoint=None#composeAuthUrl()
    def __init__(self,
        roleUrlEndpoint=roleUrlEndpoint,
        query=query,
        demo=True):
        super().__init__(cache=True)
        self.roleUrlEndpoint = roleUrlEndpoint if roleUrlEndpoint else composeAuthUrl()
        self.query = query
        self.demo = demo
        self.authorizationToken = ""

    def setTokenByInfo(self, info): self.authorizationToken = ""

    async def _load(self, id):
        variables = {"id": f"{id}"}
        if self.authorizationToken != "":
            headers = {"authorization": f"Bearer {self.authorizationToken}"}
        else:
            headers = {}
        json = {
            "query": self.query,
            "variables": variables
        }
        roleUrlEndpoint=self.roleUrlEndpoint
        async with aiohttp.ClientSession() as session:
            print(f"query {roleUrlEndpoint} for json={json}")
            async with session.post(url=roleUrlEndpoint, json=json, headers=headers) as resp:
                print(resp.status)
                if resp.status != 200:
                    text = await resp.text()
                    print(text)
                    return []
                else:
                    respJson = await resp.json()

        # print(20*"respJson")
        # print(respJson)
        
        assert respJson.get("errors", None) is None, respJson["errors"]
        respdata = respJson.get("data", None)
        assert respdata is not None, "missing data response"
        result = respdata.get("result", None)
        assert result is not None, "missing result"
        roles = result.get("roles", None)
        assert roles is not None, "missing roles"
        
        # print(30*"=")
        # print(roles)
        # print(30*"=")
        return [*roles]


    async def batch_load_fn(self, keys):
        #print('batch_load_fn', keys, flush=True)
        reducedkeys = set(keys)
        awaitables = (self._load(key) for key in reducedkeys)
        results = await asyncio.gather(*awaitables)
        indexedResult = {key:result for key, result in zip(reducedkeys, results)}
        results = [indexedResult[key] for key in keys]
        return results
    
    
###

class Loaders:
    # authorizationgroups = None
    # authorizationroletypes = None
    # authorizationusers = None
    authorizations = None
    workflows = None
    workflowstates = None
    workflowstateroletypes = None
    workflowstateusers = None
    workflowtransitions = None

    pass


### 

def createLoaders(asyncSessionMaker, models=dbmodels) -> Loaders:
    class Loaders:
        
        @property
        @cache
        def authorizations(self): return AuthorizationLoader()
        
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


from functools import cache



demouser = {
    "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
    "name": "John",
    "surname": "Newbie",
    "email": "john.newbie@world.com",
    "roles": [
        {
            "valid": True,
            "group": {
                "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                "name": "Uni"
            },
            "roletype": {
                "id": "ced46aa4-3217-4fc1-b79d-f6be7d21c6b6",
                "name": "administrátor"
            }
        },
        {
            "valid": True,
            "group": {
                "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                "name": "Uni"
            },
            "roletype": {
                "id": "ae3f0d74-6159-11ed-b753-0242ac120003",
                "name": "rektor"
            }
        }
    ]
}


def getUserFromInfo(info):
    context = info.context
    #print(list(context.keys()))
    user = context.get("user", None)
    if user is None:
        request = context.get("request", None)
        assert request is not None, "request is missing in context :("
        user = request.scope.get("user", None)
        assert user is not None, "missing user in context or in request.scope"
    logging.debug("getUserFromInfo", user)
    return user


def getAuthorizationToken(info):
    context = info.context
    request = context.get("request", None)
    assert request is not None, "trying to get authtoken from None request"

def getGroupFromInfo(info):
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
    return {
        "loaders": createLoaders(asyncSessionMaker)
    }
    
    
def createUgConnectionContext(request):
    from .gql_ug_proxy import get_ug_connection
    connection = get_ug_connection(request=request)
    return {
        "ug_connection": connection
    }
    

def getUgConnection(info):
    context = info.context
    print("getUgConnection.context", context)
    connection = context.get("ug_connection", None)
    return connection