from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import (
    createEntityByIdGetter,
    createEntityGetter,
    createInsertResolver,
)

from DBDefinitions import WorkflowModel, AuthorizationModel

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery

from DBDefinitions import WorkflowModel, AuthorizationModel

## workflow resolvers
resolveWorkflowsPaged = createEntityGetter(WorkflowModel)
resolveWorkflowById = createEntityByIdGetter(WorkflowModel)
resolveInsertWorkflow = createInsertResolver(WorkflowModel)

## authorization resolvers
resolveAuthorizationsPaged = createEntityGetter(AuthorizationModel)
resolveAuthorizationById = createEntityByIdGetter(AuthorizationModel)
resolveInsertAuthorization = createInsertResolver(AuthorizationModel)
