from __future__ import annotations
from .general import MaleoIdentityGeneralTransfers
from .parameters import MaleoIdentityParametersTransfers
from .results import MaleoIdentityResultsTransfers

class MaleoIdentityTransfers:
    General = MaleoIdentityGeneralTransfers
    Parameters = MaleoIdentityParametersTransfers
    Results = MaleoIdentityResultsTransfers