from __future__ import annotations
from .client import MaleoMetadataClientResultsTransfers
from .general import MaleoMetadataGeneralResultsTransfers
from .repository import MaleoMetadataRepositoryResultsTransfers

class MaleoMetadataResultsTransfers:
    Client = MaleoMetadataClientResultsTransfers
    General = MaleoMetadataGeneralResultsTransfers
    Repository = MaleoMetadataRepositoryResultsTransfers