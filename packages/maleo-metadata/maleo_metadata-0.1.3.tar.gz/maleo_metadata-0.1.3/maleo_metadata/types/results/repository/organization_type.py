from typing import Union
from maleo_metadata.models.transfers.results.repository.organization_type import MaleoMetadataOrganizationTypeRepositoryResultsTransfers

class MaleoMetadataOrganizationTypeRepositoryResultsTypes:
    GetMultiple = Union[
        MaleoMetadataOrganizationTypeRepositoryResultsTransfers.Fail,
        MaleoMetadataOrganizationTypeRepositoryResultsTransfers.NoData,
        MaleoMetadataOrganizationTypeRepositoryResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoMetadataOrganizationTypeRepositoryResultsTransfers.Fail,
        MaleoMetadataOrganizationTypeRepositoryResultsTransfers.NoData,
        MaleoMetadataOrganizationTypeRepositoryResultsTransfers.SingleData
    ]