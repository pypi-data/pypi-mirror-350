from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.repository import BaseServiceRepositoryResultsTransfers
from maleo_metadata.models.transfers.general.blood_type import BloodTypeTransfers

class MaleoMetadataBloodTypeRepositoryResultsTransfers:
    class Fail(BaseServiceRepositoryResultsTransfers.Fail): pass

    class NoData(BaseServiceRepositoryResultsTransfers.NoData): pass

    class SingleData(BaseServiceRepositoryResultsTransfers.SingleData):
        data:BloodTypeTransfers = Field(..., description="Single blood type data")

    class MultipleData(BaseServiceRepositoryResultsTransfers.UnpaginatedMultipleData):
        data:list[BloodTypeTransfers] = Field(..., description="Multiple blood types data")