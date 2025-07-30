from pydantic import Field
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_foundation.models.schemas.result import BaseResultSchemas
from maleo_metadata.enums.gender import MaleoMetadataGenderEnums

class MaleoMetadataGenderSchemas:
    class IdentifierType(BaseParameterSchemas.IdentifierType):
        identifier:MaleoMetadataGenderEnums.IdentifierType = Field(..., description="Gender's identifier type")

    class Key(BaseResultSchemas.Key):
        key:str = Field(..., max_length=20, description="Gender's key")

    class Name(BaseResultSchemas.Name):
        name:str = Field(..., max_length=20, description="Gender's name")