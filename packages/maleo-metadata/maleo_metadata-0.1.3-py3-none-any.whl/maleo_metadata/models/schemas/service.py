from pydantic import Field
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_foundation.models.schemas.result import BaseResultSchemas
from maleo_metadata.enums.service import MaleoMetadataServiceEnums

class MaleoMetadataServiceSchemas:
    class IdentifierType(BaseParameterSchemas.IdentifierType):
        identifier:MaleoMetadataServiceEnums.IdentifierType = Field(..., description="Service's identifier type")

    class Key(BaseResultSchemas.Key):
        key:str = Field(..., max_length=20, description="Service's key")

    class Name(BaseResultSchemas.Name):
        name:str = Field(..., max_length=20, description="Service's name")