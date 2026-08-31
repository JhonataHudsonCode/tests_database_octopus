from __future__ import annotations

from dataclasses import dataclass

## olaa
@dataclass(frozen=True, slots=True)
class ClientMetadata:
    client_id: str
    has_rsa: bool
    has_alerts: bool
    octopus_endpoint: str
