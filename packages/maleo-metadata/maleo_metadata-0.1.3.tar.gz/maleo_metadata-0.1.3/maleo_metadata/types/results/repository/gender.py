from typing import Union
from maleo_metadata.models.transfers.results.repository.gender import MaleoMetadataGenderRepositoryResultsTransfers

class MaleoMetadataGenderRepositoryResultsTypes:
    GetMultiple = Union[
        MaleoMetadataGenderRepositoryResultsTransfers.Fail,
        MaleoMetadataGenderRepositoryResultsTransfers.NoData,
        MaleoMetadataGenderRepositoryResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoMetadataGenderRepositoryResultsTransfers.Fail,
        MaleoMetadataGenderRepositoryResultsTransfers.NoData,
        MaleoMetadataGenderRepositoryResultsTransfers.SingleData
    ]