from typing import Union
from maleo_metadata.models.transfers.results.general.blood_type import MaleoMetadataBloodTypeGeneralResultsTransfers

class MaleoMetadataBloodTypeGeneralResultsTypes:
    GetMultiple = Union[
        MaleoMetadataBloodTypeGeneralResultsTransfers.Fail,
        MaleoMetadataBloodTypeGeneralResultsTransfers.NoData,
        MaleoMetadataBloodTypeGeneralResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoMetadataBloodTypeGeneralResultsTransfers.Fail,
        MaleoMetadataBloodTypeGeneralResultsTransfers.NoData,
        MaleoMetadataBloodTypeGeneralResultsTransfers.SingleData
    ]