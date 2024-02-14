import sqlalchemy
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .uuid import UUIDColumn, UUIDFKey
from .Base import BaseModel


class WorkflowTransitionModel(BaseModel):
    """zmena stav - prechod (hrana)"""

    __tablename__ = "awworkflowtransitions"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    valid = Column(Boolean, default=True, comment="if this entity is valid or invalid")
    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")

    workflow_id = Column(ForeignKey("awworkflows.id"), index=True, comment="Id of the workflow")
    sourcestate_id = Column(ForeignKey("awworkflowstates.id"), index=True, comment="Id of the first state(source)")
    destinationstate_id = Column(ForeignKey("awworkflowstates.id"), index=True, comment="Id of the second state(destination)")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Date and time the record was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(),comment="Date and time of last change")
    createdby = UUIDFKey(nullable=True, comment="who has created the entity")
                #Column(ForeignKey("users.id"), index=True, nullable=True, comment="who has created the entity")
    changedby = UUIDFKey(nullable=True, comment="who has changed this entity")
                #Column(ForeignKey("users.id"), index=True, nullable=True, comment="who has changed this entity")

