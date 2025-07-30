from typing import Union
from maleo_metadata.models.transfers.results.general.medical_role import MaleoMetadataMedicalRoleGeneralResultsTransfers

class MaleoMetadataMedicalRoleGeneralResultsTypes:
    GetMultiple = Union[
        MaleoMetadataMedicalRoleGeneralResultsTransfers.Fail,
        MaleoMetadataMedicalRoleGeneralResultsTransfers.NoData,
        MaleoMetadataMedicalRoleGeneralResultsTransfers.MultipleData
    ]

    GetStructuredMultiple = Union[
        MaleoMetadataMedicalRoleGeneralResultsTransfers.Fail,
        MaleoMetadataMedicalRoleGeneralResultsTransfers.NoData,
        MaleoMetadataMedicalRoleGeneralResultsTransfers.MultipleStructured
    ]

    GetSingle = Union[
        MaleoMetadataMedicalRoleGeneralResultsTransfers.Fail,
        MaleoMetadataMedicalRoleGeneralResultsTransfers.NoData,
        MaleoMetadataMedicalRoleGeneralResultsTransfers.SingleData
    ]

    GetSingleStructured = Union[
        MaleoMetadataMedicalRoleGeneralResultsTransfers.Fail,
        MaleoMetadataMedicalRoleGeneralResultsTransfers.NoData,
        MaleoMetadataMedicalRoleGeneralResultsTransfers.SingleStructured
    ]