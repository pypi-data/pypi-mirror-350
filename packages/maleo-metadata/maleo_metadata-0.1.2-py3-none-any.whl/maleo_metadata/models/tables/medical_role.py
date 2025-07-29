from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String
from maleo_metadata.db import MaleoMetadataMetadataManager

class MedicalRolesTable(MaleoMetadataMetadataManager.Base):
    __tablename__ = "medical_roles"
    parent_id = Column(
        "parent_id",
        Integer,
        ForeignKey(
            "medical_roles.id",
            ondelete="SET NULL",
            onupdate="CASCADE"
        )
    )
    order = Column(name="order", type_=Integer)
    code = Column(name="code", type_=String(20), unique=True, nullable=False)
    key = Column(name="key", type_=String(255), unique=True, nullable=False)
    name = Column(name="name", type_=String(255), unique=True, nullable=False)
    parent = relationship(
        "MedicalRolesTable",
        remote_side="MedicalRolesTable.id",
        back_populates="specializations"
    )
    specializations = relationship(
        "MedicalRolesTable",
        back_populates="parent",
        cascade="all, delete-orphan",
        lazy="select",
        foreign_keys="[MedicalRolesTable.parent_id]",
        order_by="MedicalRolesTable.order"
    )