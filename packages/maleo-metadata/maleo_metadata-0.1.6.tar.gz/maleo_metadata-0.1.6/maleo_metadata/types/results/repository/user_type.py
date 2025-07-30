from typing import Union
from maleo_metadata.models.transfers.results.repository.user_type import MaleoMetadataUserTypeRepositoryResultsTransfers

class MaleoMetadataUserTypeRepositoryResultsTypes:
    GetMultiple = Union[
        MaleoMetadataUserTypeRepositoryResultsTransfers.Fail,
        MaleoMetadataUserTypeRepositoryResultsTransfers.NoData,
        MaleoMetadataUserTypeRepositoryResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoMetadataUserTypeRepositoryResultsTransfers.Fail,
        MaleoMetadataUserTypeRepositoryResultsTransfers.NoData,
        MaleoMetadataUserTypeRepositoryResultsTransfers.SingleData
    ]