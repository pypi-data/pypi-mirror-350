from typing import Union
from maleo_metadata.models.transfers.results.repository.blood_type import MaleoMetadataBloodTypeRepositoryResultsTransfers

class MaleoMetadataBloodTypeRepositoryResultsTypes:
    GetMultiple = Union[
        MaleoMetadataBloodTypeRepositoryResultsTransfers.Fail,
        MaleoMetadataBloodTypeRepositoryResultsTransfers.NoData,
        MaleoMetadataBloodTypeRepositoryResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoMetadataBloodTypeRepositoryResultsTransfers.Fail,
        MaleoMetadataBloodTypeRepositoryResultsTransfers.NoData,
        MaleoMetadataBloodTypeRepositoryResultsTransfers.SingleData
    ]