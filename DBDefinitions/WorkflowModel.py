import sqlalchemy
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .uuid import UUIDColumn, UUIDFKey
from .Base import BaseModel


class WorkflowModel(BaseModel):
    """Posloupnost stavu a moznosti prechodu mezi nimi (graf)"""

    __tablename__ = "awworkflows"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")
    valid = Column(Boolean, default=True, comment="if this entity is valid or invalid")
    authorization_id = Column(ForeignKey("awauthorizations.id"), index=True)
    # authorization = relationship("AuthorizationModel", back_populates="workflow")

    # states = relationship("WorkflowStateModel", back_populates="workflow")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True, comment="who has created the entity")
                #Column(ForeignKey("users.id"), index=True, nullable=True, comment="who has created the entity")
    changedby = UUIDFKey(nullable=True, comment="who has changed this entity")
                #Column(ForeignKey("users.id"), index=True, nullable=True, comment="who has changed this entity")
