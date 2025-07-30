from __future__ import annotations
from .general import MaleoIdentityGeneralResultsTypes
from .repository import MaleoIdentityRepositoryResultsTypes
from .client import MaleoIdentityClientResultsTypes

class MaleoIdentityResultsTypes:
    General = MaleoIdentityGeneralResultsTypes
    Query = MaleoIdentityRepositoryResultsTypes
    Client = MaleoIdentityClientResultsTypes