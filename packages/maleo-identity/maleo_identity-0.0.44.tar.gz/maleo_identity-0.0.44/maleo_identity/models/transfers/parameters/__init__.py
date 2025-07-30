from __future__ import annotations
from .general import MaleoIdentityGeneralParametersTransfers
from .service import MaleoIdentityServiceParametersTransfers
from .client import MaleoIdentityClientParametersTransfers

class MaleoIdentityParametersTransfers:
    General = MaleoIdentityGeneralParametersTransfers
    Service = MaleoIdentityServiceParametersTransfers
    Client = MaleoIdentityClientParametersTransfers