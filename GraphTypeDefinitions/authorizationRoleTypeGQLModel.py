import datetime
import strawberry
from typing import List, Optional, Union, Annotated
from uuid import UUID


def getLoaders(info):
    return info.context["all"]


AuthorizationGQLModel = Annotated[
    "AuthorizationGQLModel", strawberry.lazy(".authorizationGQLModel")
]
AuthorizationResultGQLModel = Annotated[
    "AuthorizationResultGQLModel", strawberry.lazy(".authorizationGQLModel")
]

RoleTypeGQLModel = Annotated["RoleTypeGQLModel", strawberry.lazy(".externals")]
GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".externals")]


@strawberry.federation.type(
    keys=["id"], description="""Entity representing an access to information"""
)
class AuthorizationRoleTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
        loader = getLoaders(info).authorizationusers
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
            result.__strawberry_definition__ = (
                cls._type_definition
            )  # some version of strawberry changed :(
        return result

    @strawberry.field(description="""Entity primary key""")
    def id(self, info: strawberry.types.Info) -> UUID:
        return self.id

    @strawberry.field(description="""Read, write, or other?""")
    def accesslevel(self, info: strawberry.types.Info) -> int:
        return self.accesslevel

    @strawberry.field(
        description="""To which authorization this access definition belongs"""
    )
    async def authorization(
        self, info: strawberry.types.Info
    ) -> Optional["AuthorizationGQLModel"]:
        result = await AuthorizationGQLModel.resolve_reference(
            info, self.authorization_id
        )
        return result

    @strawberry.field(
        description="""Role type which user must play in the group to have this access"""
    )
    async def role_type(
        self, info: strawberry.types.Info
    ) -> Optional["RoleTypeGQLModel"]:
        result = RoleTypeGQLModel(id=self.roletype_id)
        return result

    @strawberry.field(
        description="""Group where the user having appropriate role has this access"""
    )
    async def group(self, info: strawberry.types.Info) -> Optional["GroupGQLModel"]:
        result = GroupGQLModel(id=self.group_id)
        return result


#####################################################################
#
# Special fields for query
#
#####################################################################


#####################################################################
#
# Mutation section
#
#####################################################################


@strawberry.input
class AuthorizationAddRoleGQLModel:
    authorization_id: UUID
    roletype_id: UUID
    group_id: UUID
    accesslevel: int


@strawberry.input
class AuthorizationRemoveRoleGQLModel:
    authorization_id: UUID
    role_type_id: UUID
    group_id: UUID


@strawberry.mutation(
    description="""Adds or updates a roletype at group at the authorization"""
)
async def authorization_add_role(
    self, info: strawberry.types.Info, authorization: AuthorizationAddRoleGQLModel
) -> Optional["AuthorizationResultGQLModel"]:
    loader = getLoaders(info).authorizationroles
    existing = await loader.filter_by(
        authorization_id=authorization.authorization_id,
        group_id=authorization.group_id,
        roletype_id=authorization.roletype_id,
    )
    result = AuthorizationResultGQLModel()
    result.msg = "ok"
    row = next(existing, None)
    if row is None:
        row = await loader.insert(authorization)
        result.id = authorization.authorization_id
    else:
        row = await loader.update(row, {"accesslevel": authorization.accesslevel})
        if row is None:
            result.id = None
            result.msg = "fail"
        result.id = authorization.authorization_id
    return result


@strawberry.mutation(description="""Remove the group from the authorization""")
async def authorization_remove_role(
    self, info: strawberry.types.Info, authorization: AuthorizationAddRoleGQLModel
) -> Optional["AuthorizationResultGQLModel"]:
    loader = getLoaders(info).authorizationroles
    existing = await loader.filter_by(
        authorization_id=authorization.authorization_id,
        group_id=authorization.group_id,
        roletype_id=authorization.roletype_id,
    )
    result = AuthorizationResultGQLModel()
    if existing is None:
        result.msg = "fail"
    else:
        await loader.delete(existing.id)
        result.msg = "ok"
    return result
