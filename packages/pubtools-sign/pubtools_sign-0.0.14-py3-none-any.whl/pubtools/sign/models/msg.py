import dataclasses
from typing import Dict, Any, Optional


@dataclasses.dataclass
class MsgMessage:
    """Messaging message model."""

    headers: Dict[str, Any]
    address: str
    body: Dict[str, Any]


@dataclasses.dataclass
class MsgError:
    """Messaging error model."""

    name: str
    description: Optional[str]
    source: Any
