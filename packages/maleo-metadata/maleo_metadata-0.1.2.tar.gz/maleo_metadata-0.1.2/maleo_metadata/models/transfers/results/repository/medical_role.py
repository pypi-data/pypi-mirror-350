from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.repository import BaseServiceRepositoryResultsTransfers
from maleo_metadata.models.transfers.general.medical_role import MedicalRoleTransfers, StructuredMedicalRoleTransfers

class MaleoMetadataMedicalRoleRepositoryResultsTransfers:
    class Fail(BaseServiceRepositoryResultsTransfers.Fail): pass

    class NoData(BaseServiceRepositoryResultsTransfers.NoData): pass

    class SingleData(BaseServiceRepositoryResultsTransfers.SingleData):
        data:MedicalRoleTransfers = Field(..., description="Single medical role data")

    class SingleStructured(BaseServiceRepositoryResultsTransfers.SingleData):
        data:StructuredMedicalRoleTransfers = Field(..., description="Single structured medical role data")

    class MultipleData(BaseServiceRepositoryResultsTransfers.PaginatedMultipleData):
        data:list[MedicalRoleTransfers] = Field(..., description="Multiple medical roles data")

    class MultipleStructured(BaseServiceRepositoryResultsTransfers.PaginatedMultipleData):
        data:list[StructuredMedicalRoleTransfers] = Field(..., description="Multiple structured medical roles data")