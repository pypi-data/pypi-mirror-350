from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.repository import BaseServiceRepositoryResultsTransfers
from maleo_metadata.models.transfers.general.service import ServiceTransfers

class MaleoMetadataServiceRepositoryResultsTransfers:
    class Fail(BaseServiceRepositoryResultsTransfers.Fail): pass

    class NoData(BaseServiceRepositoryResultsTransfers.NoData): pass

    class SingleData(BaseServiceRepositoryResultsTransfers.SingleData):
        data:ServiceTransfers = Field(..., description="Single service data")

    class MultipleData(BaseServiceRepositoryResultsTransfers.UnpaginatedMultipleData):
        data:list[ServiceTransfers] = Field(..., description="Multiple services data")