from sqlalchemy import Column, Integer, String
from maleo_metadata.db import MaleoMetadataMetadataManager

class BloodTypesTable(MaleoMetadataMetadataManager.Base):
    __tablename__ = "blood_types"
    order = Column(name="order", type_=Integer)
    key = Column(name="key", type_=String(2), unique=True, nullable=False)
    name = Column(name="name", type_=String(2), unique=True, nullable=False)