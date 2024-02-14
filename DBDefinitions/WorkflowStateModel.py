import sqlalchemy
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .uuid import UUIDColumn, UUIDFKey
from .Base import BaseModel


class WorkflowStateModel(BaseModel):
    """stav v posloupnosti (vrchol)"""

    __tablename__ = "awworkflowstates"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)

    valid = Column(Boolean, default=True, comment="if this entity is valid or invalid")

    workflow_id = Column(ForeignKey("awworkflows.id"), index=True)
    # workflow = relationship("WorkflowModel", back_populates="states")
    # roletypes = relationship("WorkflowStateRoleModel", back_populates="workflowstate")
    # users = relationship("WorkflowStateUserModel", back_populates="workflowstate")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Date and time the record was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(),comment="Date and time of last change")
    changedby = UUIDFKey(nullable=True, comment="who has changed this entity")
                #Column(ForeignKey("users.id"), index=True, nullable=True, comment="who has changed this entity")
    createdby = UUIDFKey(nullable=True, comment="who has created the entity")
                #Column(ForeignKey("users.id"), index=True, nullable=True, comment="who has created the entity")

    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")
