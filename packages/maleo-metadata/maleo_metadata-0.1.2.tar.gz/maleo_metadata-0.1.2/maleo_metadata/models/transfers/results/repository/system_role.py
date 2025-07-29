from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.repository import BaseServiceRepositoryResultsTransfers
from maleo_metadata.models.transfers.general.system_role import SystemRoleTransfers

class MaleoMetadataSystemRoleRepositoryResultsTransfers:
    class Fail(BaseServiceRepositoryResultsTransfers.Fail): pass

    class NoData(BaseServiceRepositoryResultsTransfers.NoData): pass

    class SingleData(BaseServiceRepositoryResultsTransfers.SingleData):
        data:SystemRoleTransfers = Field(..., description="Single system role data")

    class MultipleData(BaseServiceRepositoryResultsTransfers.UnpaginatedMultipleData):
        data:list[SystemRoleTransfers] = Field(..., description="Multiple system roles data")