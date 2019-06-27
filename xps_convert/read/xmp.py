from dataclasses import field, dataclass
from typing import Dict


@dataclass
class Xmp:
    values: Dict[str, str] = field(default_factory=dict)
