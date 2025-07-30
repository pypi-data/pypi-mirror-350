from __future__ import annotations
from .client import MaleoIdentityClientResultsTransfers
from .general import MaleoIdentityGeneralResultsTransfers
from .repository import MaleoIdentityRepositoryResultsTransfers

class MaleoIdentityResultsTransfers:
    Client = MaleoIdentityClientResultsTransfers
    General = MaleoIdentityGeneralResultsTransfers
    Query = MaleoIdentityRepositoryResultsTransfers