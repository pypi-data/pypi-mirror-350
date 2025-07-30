from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.schemas.result import BaseResultSchemas
from maleo_metadata.models.schemas.user_type import MaleoMetadataUserTypeSchemas

class UserTypeTransfers(
    MaleoMetadataUserTypeSchemas.Name,
    MaleoMetadataUserTypeSchemas.Key,
    BaseResultSchemas.Order,
    BaseGeneralSchemas.Status,
    BaseResultSchemas.Timestamps,
    BaseResultSchemas.Identifiers
):
    pass