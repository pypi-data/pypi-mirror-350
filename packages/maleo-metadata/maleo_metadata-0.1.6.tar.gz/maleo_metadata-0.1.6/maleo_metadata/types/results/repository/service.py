from typing import Union
from maleo_metadata.models.transfers.results.repository.service import MaleoMetadataServiceRepositoryResultsTransfers

class MaleoMetadataServiceRepositoryResultsTypes:
    GetMultiple = Union[
        MaleoMetadataServiceRepositoryResultsTransfers.Fail,
        MaleoMetadataServiceRepositoryResultsTransfers.NoData,
        MaleoMetadataServiceRepositoryResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoMetadataServiceRepositoryResultsTransfers.Fail,
        MaleoMetadataServiceRepositoryResultsTransfers.NoData,
        MaleoMetadataServiceRepositoryResultsTransfers.SingleData
    ]