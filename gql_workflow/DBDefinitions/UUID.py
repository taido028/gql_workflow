from sqlalchemy import Column, String
from uuid import uuid4


def UUIDFKey(comment=None, nullable=True, **kwargs):
    return Column(String, index=True, comment=comment, nullable=nullable, **kwargs)


def UUIDColumn():
    return Column(
        String, primary_key=True, comment="primary key", default=lambda: str(uuid4())
    )
