from typing import List

from bluer_ai.host import signature as bluer_ai_signature
from bluer_flow import fullname as bluer_flow_fullname

from bluer_geo import fullname


def signature() -> List[str]:
    return [
        fullname(),
        bluer_flow_fullname(),
    ] + bluer_ai_signature()
