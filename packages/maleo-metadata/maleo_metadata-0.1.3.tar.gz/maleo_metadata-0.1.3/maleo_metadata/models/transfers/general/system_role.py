from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.schemas.result import BaseResultSchemas
from maleo_metadata.models.schemas.system_role import MaleoMetadataSystemRoleSchemas

class SystemRoleTransfers(
    MaleoMetadataSystemRoleSchemas.Name,
    MaleoMetadataSystemRoleSchemas.Key,
    BaseResultSchemas.Order,
    BaseGeneralSchemas.Status,
    BaseResultSchemas.Timestamps,
    BaseResultSchemas.Identifiers
):
    pass