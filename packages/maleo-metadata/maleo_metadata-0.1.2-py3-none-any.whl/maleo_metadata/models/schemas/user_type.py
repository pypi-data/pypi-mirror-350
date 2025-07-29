from pydantic import Field
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_foundation.models.schemas.result import BaseResultSchemas
from maleo_metadata.enums.user_type import MaleoMetadataUserTypeEnums

class MaleoMetadataUserTypeSchemas:
    class IdentifierType(BaseParameterSchemas.IdentifierType):
        identifier:MaleoMetadataUserTypeEnums.IdentifierType = Field(..., description="User Type's identifier type")

    class Key(BaseResultSchemas.Key):
        key:str = Field(..., max_length=20, description="User Type's key")

    class Name(BaseResultSchemas.Name):
        name:str = Field(..., max_length=20, description="User Type's name")