import sqlalchemy
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .uuid import UUIDColumn, UUIDFKey
from .Base import BaseModel


class WorkflowStateUserModel(BaseModel):
    """model pristupu - uzivatel + skupina"""

    __tablename__ = "awworkflowstateusers"

    id = UUIDColumn()
    name = Column(String)
    accesslevel = Column(Integer)
    valid = Column(Boolean, default=True, comment="if this entity is valid or invalid")
    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")

    workflowstate_id = Column(ForeignKey("awworkflowstates.id"), index=True)
    # workflowstate = relationship("WorkflowStateModel", back_populates="users")

    user_id = UUIDFKey(nullable=True, comment="User identifier (foreign key) with the possibility of a null value")  # Column(ForeignKey("users.id"), index=True)
    group_id = UUIDFKey(nullable=True, comment="Group identifier (foreign key) with the possibility of a null value")  # Column(ForeignKey("groups.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Date and time the record was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(),comment="Date and time of last change")
    createdby = UUIDFKey(nullable=True, comment="who has created the entity")
                #Column(ForeignKey("users.id"), index=True, nullable=True, comment="who has created the entity")
    changedby = UUIDFKey(nullable=True, comment="who has changed this entity")
                #Column(ForeignKey("users.id"), index=True, nullable=True, comment="who has changed this entity")
