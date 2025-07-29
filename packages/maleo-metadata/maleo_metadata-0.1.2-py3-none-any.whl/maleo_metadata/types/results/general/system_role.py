from typing import Union
from maleo_metadata.models.transfers.results.general.system_role import MaleoMetadataSystemRoleGeneralResultsTransfers

class MaleoMetadataSystemRoleGeneralResultsTypes:
    GetMultiple = Union[
        MaleoMetadataSystemRoleGeneralResultsTransfers.Fail,
        MaleoMetadataSystemRoleGeneralResultsTransfers.NoData,
        MaleoMetadataSystemRoleGeneralResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoMetadataSystemRoleGeneralResultsTransfers.Fail,
        MaleoMetadataSystemRoleGeneralResultsTransfers.NoData,
        MaleoMetadataSystemRoleGeneralResultsTransfers.SingleData
    ]