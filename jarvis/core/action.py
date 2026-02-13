from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Action:
    action: str
    parameters: Dict[str, Any]
