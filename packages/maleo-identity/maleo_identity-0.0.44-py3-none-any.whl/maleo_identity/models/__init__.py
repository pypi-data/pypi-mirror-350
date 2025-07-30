from __future__ import annotations
from .tables import MaleoIdentityTables
from .schemas import MaleoIdentitySchemas
from .transfers import MaleoIdentityTransfers
from .responses import MaleoIdentityResponses

class MaleoIdentityModels:
    Tables = MaleoIdentityTables
    Schemas = MaleoIdentitySchemas
    Transfers = MaleoIdentityTransfers
    Responses = MaleoIdentityResponses