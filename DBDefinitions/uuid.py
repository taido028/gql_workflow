from sqlalchemy import Column, String

from sqlalchemy import Uuid
import uuid


def newUuidAsString():
    return uuid.uuid4()


def UUIDColumn():
    return Column(Uuid, primary_key=True, comment="primary key", default=newUuidAsString())


def UUIDFKey(comment=None, nullable=True, **kwargs):
    return Column(Uuid, index=True, comment=comment, nullable=nullable, **kwargs)

