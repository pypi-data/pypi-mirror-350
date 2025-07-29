from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.schemas.result import BaseResultSchemas
from maleo_metadata.models.schemas.blood_type import MaleoMetadataBloodTypeSchemas

class BloodTypeTransfers(
    MaleoMetadataBloodTypeSchemas.Name,
    MaleoMetadataBloodTypeSchemas.Key,
    BaseResultSchemas.Order,
    BaseGeneralSchemas.Status,
    BaseResultSchemas.Timestamps,
    BaseResultSchemas.Identifiers
):
    pass