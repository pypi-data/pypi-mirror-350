from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.schemas.result import BaseResultSchemas
from maleo_metadata.models.schemas.gender import MaleoMetadataGenderSchemas

class GenderTransfers(
    MaleoMetadataGenderSchemas.Name,
    MaleoMetadataGenderSchemas.Key,
    BaseResultSchemas.Order,
    BaseGeneralSchemas.Status,
    BaseResultSchemas.Timestamps,
    BaseResultSchemas.Identifiers
):
    pass