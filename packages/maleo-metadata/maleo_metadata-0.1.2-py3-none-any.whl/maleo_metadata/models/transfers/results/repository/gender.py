from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.repository import BaseServiceRepositoryResultsTransfers
from maleo_metadata.models.transfers.general.gender import GenderTransfers

class MaleoMetadataGenderRepositoryResultsTransfers:
    class Fail(BaseServiceRepositoryResultsTransfers.Fail): pass

    class NoData(BaseServiceRepositoryResultsTransfers.NoData): pass

    class SingleData(BaseServiceRepositoryResultsTransfers.SingleData):
        data:GenderTransfers = Field(..., description="Single gender data")

    class MultipleData(BaseServiceRepositoryResultsTransfers.UnpaginatedMultipleData):
        data:list[GenderTransfers] = Field(..., description="Multiple genders data")