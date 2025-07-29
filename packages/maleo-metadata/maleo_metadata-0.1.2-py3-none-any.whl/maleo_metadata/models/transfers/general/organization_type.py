from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.schemas.result import BaseResultSchemas
from maleo_metadata.models.schemas.organization_type import MaleoMetadataOrganizationTypeSchemas

class OrganizationTypeTransfers(
    MaleoMetadataOrganizationTypeSchemas.Name,
    MaleoMetadataOrganizationTypeSchemas.Key,
    BaseResultSchemas.Order,
    BaseGeneralSchemas.Status,
    BaseResultSchemas.Timestamps,
    BaseResultSchemas.Identifiers
):
    pass