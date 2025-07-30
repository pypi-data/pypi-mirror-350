from typing import Union
from maleo_metadata.models.transfers.results.general.organization_type import MaleoMetadataOrganizationTypeGeneralResultsTransfers

class MaleoMetadataOrganizationTypeGeneralResultsTypes:
    GetMultiple = Union[
        MaleoMetadataOrganizationTypeGeneralResultsTransfers.Fail,
        MaleoMetadataOrganizationTypeGeneralResultsTransfers.NoData,
        MaleoMetadataOrganizationTypeGeneralResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoMetadataOrganizationTypeGeneralResultsTransfers.Fail,
        MaleoMetadataOrganizationTypeGeneralResultsTransfers.NoData,
        MaleoMetadataOrganizationTypeGeneralResultsTransfers.SingleData
    ]