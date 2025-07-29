from typing import Union
from maleo_metadata.models.transfers.results.repository.medical_role import MaleoMetadataMedicalRoleRepositoryResultsTransfers

class MaleoMetadataMedicalRoleRepositoryResultsTypes:
    GetMultiple = Union[
        MaleoMetadataMedicalRoleRepositoryResultsTransfers.Fail,
        MaleoMetadataMedicalRoleRepositoryResultsTransfers.NoData,
        MaleoMetadataMedicalRoleRepositoryResultsTransfers.MultipleData
    ]

    GetStructuredMultiple = Union[
        MaleoMetadataMedicalRoleRepositoryResultsTransfers.Fail,
        MaleoMetadataMedicalRoleRepositoryResultsTransfers.NoData,
        MaleoMetadataMedicalRoleRepositoryResultsTransfers.MultipleStructured
    ]

    GetSingle = Union[
        MaleoMetadataMedicalRoleRepositoryResultsTransfers.Fail,
        MaleoMetadataMedicalRoleRepositoryResultsTransfers.NoData,
        MaleoMetadataMedicalRoleRepositoryResultsTransfers.SingleData
    ]

    GetSingleStructured = Union[
        MaleoMetadataMedicalRoleRepositoryResultsTransfers.Fail,
        MaleoMetadataMedicalRoleRepositoryResultsTransfers.NoData,
        MaleoMetadataMedicalRoleRepositoryResultsTransfers.SingleStructured
    ]