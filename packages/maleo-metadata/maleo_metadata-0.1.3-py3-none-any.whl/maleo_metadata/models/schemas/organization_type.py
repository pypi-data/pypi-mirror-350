from pydantic import Field
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_foundation.models.schemas.result import BaseResultSchemas
from maleo_metadata.enums.organization_type import MaleoMetadataOrganizationTypeEnums

class MaleoMetadataOrganizationTypeSchemas:
    class IdentifierType(BaseParameterSchemas.IdentifierType):
        identifier:MaleoMetadataOrganizationTypeEnums.IdentifierType = Field(..., description="Organization Type's identifier type")

    class Key(BaseResultSchemas.Key):
        key:str = Field(..., max_length=20, description="Organization Type's key")

    class Name(BaseResultSchemas.Name):
        name:str = Field(..., max_length=20, description="Organization Type's name")