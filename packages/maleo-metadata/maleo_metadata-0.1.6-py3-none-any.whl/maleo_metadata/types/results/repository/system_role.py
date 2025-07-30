from typing import Union
from maleo_metadata.models.transfers.results.repository.system_role import MaleoMetadataSystemRoleRepositoryResultsTransfers

class MaleoMetadataSystemRoleRepositoryResultsTypes:
    GetMultiple = Union[
        MaleoMetadataSystemRoleRepositoryResultsTransfers.Fail,
        MaleoMetadataSystemRoleRepositoryResultsTransfers.NoData,
        MaleoMetadataSystemRoleRepositoryResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoMetadataSystemRoleRepositoryResultsTransfers.Fail,
        MaleoMetadataSystemRoleRepositoryResultsTransfers.NoData,
        MaleoMetadataSystemRoleRepositoryResultsTransfers.SingleData
    ]