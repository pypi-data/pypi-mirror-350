from sqlalchemy import Column, Integer, String
from maleo_metadata.db import MaleoMetadataMetadataManager

class GendersTable(MaleoMetadataMetadataManager.Base):
    __tablename__ = "genders"
    order = Column(name="order", type_=Integer)
    key = Column(name="key", type_=String(20), unique=True, nullable=False)
    name = Column(name="name", type_=String(20), unique=True, nullable=False)