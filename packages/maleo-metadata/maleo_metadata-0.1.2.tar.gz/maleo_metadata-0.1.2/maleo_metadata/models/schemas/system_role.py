from pydantic import Field
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_foundation.models.schemas.result import BaseResultSchemas
from maleo_metadata.enums.system_role import MaleoMetadataSystemRoleEnums

class MaleoMetadataSystemRoleSchemas:
    class IdentifierType(BaseParameterSchemas.IdentifierType):
        identifier:MaleoMetadataSystemRoleEnums.IdentifierType = Field(..., description="System Role's identifier type")

    class Key(BaseResultSchemas.Key):
        key:str = Field(..., max_length=20, description="System Role's key")

    class Name(BaseResultSchemas.Name):
        name:str = Field(..., max_length=20, description="System Role's name")