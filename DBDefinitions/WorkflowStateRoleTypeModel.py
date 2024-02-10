import sqlalchemy
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .uuid import UUIDColumn, UUIDFKey
from .Base import BaseModel


class WorkflowStateRoleTypeModel(BaseModel):
    """model pristupu - role, kterou musi splnovat"""

    __tablename__ = "awworkflowstateroletypes"

    id = UUIDColumn()
    name = Column(String)
    accesslevel = Column(Integer)
    valid = Column(Boolean, default=True, comment="if this entity is valid or invalid")
    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")

    workflowstate_id = Column(ForeignKey("awworkflowstates.id"), index=True)
    # workflowstate = relationship("WorkflowStateModel", back_populates="roletypes")

    roletype_id = UUIDFKey(
        nullable=True
    )  # Column(ForeignKey("roletypes.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    changedby = UUIDFKey(
        nullable=True
    )  # Column(ForeignKey("users.id"), index=True, nullable=True)
    createdby = UUIDFKey(
        nullable=True
    )  # Column(ForeignKey("users.id"), index=True, nullable=True)
