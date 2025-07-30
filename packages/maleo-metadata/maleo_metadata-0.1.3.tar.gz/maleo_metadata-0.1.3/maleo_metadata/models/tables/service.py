from sqlalchemy import Column, Integer, UUID, String
from uuid import uuid4
from maleo_metadata.db import MaleoMetadataMetadataManager

class ServicesTable(MaleoMetadataMetadataManager.Base):
    __tablename__ = "services"
    order = Column(name="order", type_=Integer)
    key = Column(name="key", type_=String(20), unique=True, nullable=False)
    name = Column(name="name", type_=String(20), unique=True, nullable=False)
    secret = Column(name="secret", type_=UUID, default=uuid4, unique=True, nullable=False)