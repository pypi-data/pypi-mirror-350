from dataclasses import dataclass
from typing import Optional


@dataclass(kw_only=True)
class CustomerDevice:
    ipAddress: Optional[str] = None
    deviceToken: Optional[str] = None
