import strawberry
import uuid
import datetime
from typing import List, Optional, Union, Annotated
import typing

UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".externals")]
GroupGQLModel = typing.Annotated["GroupGQLModel", strawberry.lazy(".externals")]
RoleTypeGQLModel = typing.Annotated["RoleTypeGQLModel", strawberry.lazy(".externals")]

from ._GraphPermissions import OnlyForAuthentized



@strawberry.field(description="""Entity primary key""", permission_classes=[OnlyForAuthentized()])
def resolve_id(self) -> uuid.UUID:
    return self.id


@strawberry.field(description="""workflow id """, permission_classes=[OnlyForAuthentized()])
def resolve_workflow_id(self) -> uuid.UUID:
    return self.workflow_id


async def resolve_group(group_id):
    from .externals import GroupGQLModel
    result = None if group_id is None else await GroupGQLModel.resolve_reference(group_id)
    return result


@strawberry.field(description="""Group ID""", permission_classes=[OnlyForAuthentized()])
async def resolve_group_id(self) -> typing.Optional["GroupGQLModel"]:
    return await resolve_group(self.group_id)


async def resolve_user(user_id):
    from .externals import UserGQLModel
    result = None if user_id is None else await UserGQLModel.resolve_reference(user_id)
    return result


@strawberry.field(description="""User ID """, permission_classes=[OnlyForAuthentized()])
async def resolve_user_id(self) -> typing.Optional["UserGQLModel"]:
    return await resolve_user(self.user_id)


async def resolve_roletype(roletype_id):
    from .externals import RoleTypeGQLModel
    result = None if roletype_id is None else await RoleTypeGQLModel.resolve_reference(roletype_id)
    return result

@strawberry.field(description="""Role Type ID """, permission_classes=[OnlyForAuthentized()])
async def resolve_roletype_id(self) -> typing.Optional["RoleTypeGQLModel"]:
    return await resolve_roletype(self.roletype_id)


@strawberry.field(description="""Level of authorization""", permission_classes=[OnlyForAuthentized()])
def resolve_accesslevel(self) -> int:
    return self.accesslevel


@strawberry.field(description="""Time of last update""", permission_classes=[OnlyForAuthentized()])
def resolve_lastchange(self) -> datetime.datetime:
    return self.lastchange

@strawberry.field(description="""Name of the workflow""", permission_classes=[OnlyForAuthentized()])
def resolve_name(self) -> str:
    return self.name

@strawberry.field(description="""if the state is enabled""", permission_classes=[OnlyForAuthentized()])
def resolve_valid(self) -> Optional[bool]:
    return self.valid if self.valid is not None else False


@strawberry.field(description="""Time of entity introduction""", permission_classes=[OnlyForAuthentized()])
def resolve_created(self) -> typing.Optional[datetime.datetime]:
    return self.created


@strawberry.field(description="""Who created entity""", permission_classes=[OnlyForAuthentized()])
async def resolve_createdby(self) -> typing.Optional["UserGQLModel"]:
    return await resolve_user(self.created_by)


@strawberry.field(description="""Who made last change""", permission_classes=[OnlyForAuthentized()])
async def resolve_changedby(self) -> typing.Optional["UserGQLModel"]:
    return await resolve_user(self.changedby)

RBACObjectGQLModel = typing.Annotated["RBACObjectGQLModel", strawberry.lazy(".externals")]
@strawberry.field(description="""Who made last change""",
        permission_classes=[OnlyForAuthentized()])
async def resolve_rbacobject(self, info: strawberry.types.Info) -> typing.Optional[RBACObjectGQLModel]:
    from .externals import RBACObjectGQLModel
    result = None if self.rbacobject is None else await RBACObjectGQLModel.resolve_reference(info, self.rbacobject)
    return result


resolve_result_id: uuid.UUID = strawberry.field(description="primary key of CU operation object")
resolve_result_msg: str = strawberry.field(description="""Should be `ok` if descired state has been reached, otherwise `fail`.
For update operation fail should be also stated when bad lastchange has been entered.""")

# fields for mutations insert and update
resolve_insert_id = strawberry.field(graphql_type=typing.Optional[uuid.UUID], description="primary key (UUID), could be client generated", default=None)
resolve_update_id = strawberry.field(graphql_type=uuid.UUID, description="primary key (UUID), identifies object of operation")
resolve_update_lastchage = strawberry.field(graphql_type=datetime.datetime, description="timestamp of last change = TOKEN")

# fields for mutation result
resolve_cu_result_id = strawberry.field(graphql_type=uuid.UUID, description="primary key of CU operation object")
resolve_cu_result_msg = strawberry.field(graphql_type=str, description="""Should be `ok` if descired state has been reached, otherwise `fail`.
For update operation fail should be also stated when bad lastchange has been entered.""")

from inspect import signature
import inspect 
from functools import wraps

# def asPage(field, *, extendedfilter=None):
#     def decorator(field):
#         print(field.__name__, field.__annotations__)
#         signatureField = signature(field)
#         return_annotation = signatureField.return_annotation

#         skipParameter = signatureField.parameters.get("skip", None)
#         skipParameterDefault = 0
#         if skipParameter:
#             skipParameterDefault = skipParameter.default

#         limitParameter = signatureField.parameters.get("limit", None)
#         limitParameterDefault = 10
#         if limitParameter:
#             limitParameterDefault = limitParameter.default

#         whereParameter = signatureField.parameters.get("where", None)
#         whereParameterDefault = None
#         whereParameterAnnotation = str
#         if whereParameter:
#             whereParameterDefault = whereParameter.default
#             whereParameterAnnotation = whereParameter.annotation

#         async def foreignkeyVectorSimple(
#             self, info: strawberry.types.Info,
#             skip: typing.Optional[int] = skipParameterDefault,
#             limit: typing.Optional[int] = limitParameterDefault
#         ) -> signature(field).return_annotation:
#             loader = await field(self, info)
#             results = await loader.page(skip=skip, limit=limit, extendedfilter=extendedfilter)
#             return results
#         foreignkeyVectorSimple.__name__ = field.__name__
#         foreignkeyVectorSimple.__doc__ = field.__doc__

#         async def foreignkeyVectorComplex(
#             self, info: strawberry.types.Info, 
#             where: whereParameterAnnotation = None, 
#             #where: typing.Optional[whereParameterAnnotation] = whereParameterDefault, 
#             #where: typing.Optional[str] = None, 
#             orderby: typing.Optional[str] = None, 
#             desc: typing.Optional[bool] = None, 
#             skip: typing.Optional[int] = skipParameterDefault,
#             limit: typing.Optional[int] = limitParameterDefault
#         ) -> signatureField.return_annotation:
#             # logging.info(f"waiting for a loader {where}")
#             wf = None if where is None else strawberry.asdict(where)
#             loader = await field(self, info, where=wf)
#             results = await loader.page(skip=skip, limit=limit, where=wf, orderby=orderby, desc=desc, extendedfilter=extendedfilter)


#             return results
#         foreignkeyVectorComplex.__name__ = field.__name__
#         foreignkeyVectorComplex.__doc__ = field.__doc__
        
#         if return_annotation._name == "List":
#             return foreignkeyVectorComplex if whereParameter else foreignkeyVectorSimple
#         else:
#             raise Exception("Unable to recognize decorated function, I am sorry")

#     return decorator(field) if field else decorator

# def asForeignList(*, foreignKeyName: str):
#     assert foreignKeyName is not None, "foreignKeyName must be defined"
#     def decorator(field):
#         print(field.__name__, field.__annotations__)
#         signatureField = signature(field)
#         return_annotation = signatureField.return_annotation

#         skipParameter = signatureField.parameters.get("skip", None)
#         skipParameterDefault = skipParameter.default if skipParameter else 0

#         limitParameter = signatureField.parameters.get("limit", None)
#         limitParameterDefault = limitParameter.default if limitParameter else 10

#         whereParameter = signatureField.parameters.get("where", None)
#         whereParameterDefault = whereParameter.default if whereParameter else None
#         whereParameterAnnotation = whereParameter.annotation if whereParameter else str

#         async def foreignkeyVectorSimple(
#             self, info: strawberry.types.Info,
#             skip: typing.Optional[int] = skipParameterDefault,
#             limit: typing.Optional[int] = limitParameterDefault
#         ) -> signature(field).return_annotation:
#             extendedfilter = {}
#             extendedfilter[foreignKeyName] = self.id
#             loader = field(self, info)
#             if inspect.isawaitable(loader):
#                 loader = await loader
#             results = await loader.page(skip=skip, limit=limit, extendedfilter=extendedfilter)
#             return results
#         foreignkeyVectorSimple.__name__ = field.__name__
#         foreignkeyVectorSimple.__doc__ = field.__doc__
#         foreignkeyVectorSimple.__module__ = field.__module__

#         async def foreignkeyVectorComplex(
#             self, info: strawberry.types.Info, 
#             where: whereParameterAnnotation = whereParameterDefault, 
#             orderby: typing.Optional[str] = None, 
#             desc: typing.Optional[bool] = None, 
#             skip: typing.Optional[int] = skipParameterDefault,
#             limit: typing.Optional[int] = limitParameterDefault
#         ) -> signatureField.return_annotation:
#             extendedfilter = {}
#             extendedfilter[foreignKeyName] = self.id
#             loader = field(self, info)
#             if inspect.isawaitable(loader):
#                 loader = await loader
            
#             wf = None if where is None else strawberry.asdict(where)
#             results = await loader.page(skip=skip, limit=limit, where=wf, orderby=orderby, desc=desc, extendedfilter=extendedfilter)
#             return results
#         foreignkeyVectorComplex.__name__ = field.__name__
#         foreignkeyVectorComplex.__doc__ = field.__doc__
#         foreignkeyVectorComplex.__module__ = field.__module__

#         async def foreignkeyVectorComplex2(
#             self, info: strawberry.types.Info, 
#             where: whereParameterAnnotation = whereParameterDefault, 
#             orderby: typing.Optional[str] = None, 
#             desc: typing.Optional[bool] = None, 
#             skip: typing.Optional[int] = skipParameterDefault,
#             limit: typing.Optional[int] = limitParameterDefault
#         ) -> signatureField.return_annotation: #typing.List[str]:
#             extendedfilter = {}
#             extendedfilter[foreignKeyName] = self.id
#             loader = field(self, info)
            
#             wf = None if where is None else strawberry.asdict(where)
#             results = await loader.page(skip=skip, limit=limit, where=wf, orderby=orderby, desc=desc, extendedfilter=extendedfilter)
#             return results
#         foreignkeyVectorComplex2.__module__ = field.__module__
#         if return_annotation._name == "List":
#             return foreignkeyVectorComplex if whereParameter else foreignkeyVectorSimple
#         else:
#             raise Exception("Unable to recognize decorated function, I am sorry")

#     return decorator


def createAttributeScalarResolver(
    scalarType: None = None,
    foreignKeyName: str = None,
    description="Retrieves item by its id",
    permission_classes=()
):
    assert scalarType is not None
    assert foreignKeyName is not None

    @strawberry.field(description=description, permission_classes=permission_classes)
    async def foreignkeyScalar(
        self, info: strawberry.types.Info
    ) -> typing.Optional[scalarType]:
        # 👇 self must have an attribute, otherwise it is fail of definition
        assert hasattr(self, foreignKeyName)
        id = getattr(self, foreignKeyName, None)

        result = None if id is None else await scalarType.resolve_reference(info=info, id=id)
        return result

    return foreignkeyScalar


def createAttributeVectorResolver(
    scalarType: None = None,
    whereFilterType: None = None,
    foreignKeyName: str = None,
    loaderLambda=lambda info: None,
    description="Retrieves items paged",
    skip: int = 0,
    limit: int = 10):
    assert scalarType is not None
    assert foreignKeyName is not None

    @strawberry.field(description=description)
    async def foreignkeyVector(
            self, info: strawberry.types.Info,
            skip: int = skip,
            limit: int = limit,
            where: typing.Optional[whereFilterType] = None
    ) -> typing.List[scalarType]:
        params = {foreignKeyName: self.id}
        loader = loaderLambda(info)
        assert loader is not None

        wf = None if where is None else strawberry.asdict(where)
        result = await loader.page(skip=skip, limit=limit, where=wf, extendedfilter=params)
        return result

    return foreignkeyVector


def createRootResolver_by_id(scalarType: None, description="Retrieves item by its id"):
    assert scalarType is not None

    @strawberry.field(description=description, permission_classes=[OnlyForAuthentized()])
    async def by_id(
            self, info: strawberry.types.Info, id: uuid.UUID
    ) -> typing.Optional[scalarType]:
        print(f"Received ID: {id}")
        try:
            result = await scalarType.resolve_reference(info=info, id=id)
            print(f"Query result: {result}")
            return result
        except Exception as e:
            print(f"Error in resolver: {e}")
            return None
    return by_id


def createRootResolver_by_page(
        scalarType: None,
        whereFilterType: None,
        loaderLambda=lambda info: None,
        description="Retrieves items paged",
        skip: int = 0,
        limit: int = 10):
    assert scalarType is not None
    assert whereFilterType is not None

    @strawberry.field(description=description, permission_classes=[OnlyForAuthentized(isList=True)])
    #@asPage
    async def paged(
            self, info: strawberry.types.Info,
            skip: int = skip, limit: int = limit, where: typing.Optional[whereFilterType] = None
    ) -> typing.List[scalarType]:
        loader = loaderLambda(info)
        assert loader is not None
        wf = None if where is None else strawberry.asdict(where)
        result = await loader.page(skip=skip, limit=limit, where=wf)
        return result

    return paged