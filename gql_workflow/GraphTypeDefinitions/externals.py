import datetime
import strawberry
from typing import List, Optional, Union, Annotated
from uuid import UUID


def getLoaders(info):
    return info.context["all"]


@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    id: UUID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: UUID):
        return UserGQLModel(id=id)


@strawberry.federation.type(extend=True, keys=["id"])
class RoleTypeGQLModel:
    id: UUID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: UUID):
        return RoleTypeGQLModel(id=id)


@strawberry.federation.type(extend=True, keys=["id"])
class GroupGQLModel:
    id: UUID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: UUID):
        return GroupGQLModel(id=id)
