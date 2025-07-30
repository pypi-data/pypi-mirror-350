from dataclasses import dataclass

@dataclass
class NetworkService:
    """Represents a discovered network service."""
    ip: str
    port: int
    service: str = "unknown"
    protocol: str = "tcp"
    banner: str = ""
    is_secure: bool = False
    is_up: bool = True
