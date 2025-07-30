"""
Data models for network scanning functionality.
"""
from dataclasses import dataclass, field
from enum import Enum
from ipaddress import ip_address, IPv4Address, IPv6Address
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any, Set
import time


class Protocol(str, Enum):
    """Network protocols."""
    TCP = "tcp"
    UDP = "udp"


class ServiceStatus(str, Enum):
    """Service status enumeration."""
    UP = "up"
    DOWN = "down"
    UNKNOWN = "unknown"


class NetworkService(BaseModel):
    """
    Represents a discovered network service.
    
    Attributes:
        ip: IP address of the service (IPv4 or IPv6)
        port: Port number (1-65535)
        service: Service identifier (e.g., 'http', 'ssh')
        protocol: Network protocol (tcp/udp)
        banner: Banner information if available
        is_secure: Whether the connection is secure
        status: Service status (up/down/unknown)
        metadata: Additional service metadata
    """
    ip: str
    port: int = Field(..., ge=1, le=65535)
    service: str = "unknown"
    protocol: Protocol = Protocol.TCP
    banner: str = ""
    is_secure: bool = False
    status: ServiceStatus = ServiceStatus.UNKNOWN
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('ip')
    def validate_ip(cls, v):
        """Validate IP address format."""
        try:
            ip_address(v)
            return v
        except ValueError:
            raise ValueError(f"Invalid IP address: {v}")
    
    @validator('service')
    def validate_service(cls, v):
        """Normalize service name."""
        return v.lower().strip()
    
    class Config:
        json_encoders = {
            Protocol: lambda p: p.value,
            ServiceStatus: lambda s: s.value
        }
        use_enum_values = True


class ScanResult(BaseModel):
    """
    Container for scan results with additional metadata.
    
    Attributes:
        services: List of discovered services
        duration_seconds: Duration of the scan in seconds
        target: The target that was scanned (IP or hostname)
        timestamp: When the scan was performed
    """
    services: List[NetworkService] = Field(default_factory=list)
    duration_seconds: float = Field(..., ge=0.0)
    target: str
    timestamp: float = Field(default_factory=lambda: time.time())
    
    @property
    def total_ports(self) -> int:
        """Total number of ports scanned."""
        return len(self.services)
    
    @property
    def open_ports(self) -> int:
        """Number of open ports found."""
        return sum(1 for s in self.services if s.status == ServiceStatus.UP)
    
    @property
    def open_services(self) -> List[NetworkService]:
        """List of services that are currently up."""
        return [s for s in self.services if s.status == ServiceStatus.UP]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert results to a dictionary."""
        return {
            'target': self.target,
            'timestamp': self.timestamp,
            'duration_seconds': self.duration_seconds,
            'total_ports': self.total_ports,
            'open_ports': self.open_ports,
            'services': [s.dict() for s in self.services]
        }
    
    def to_json(self, **kwargs) -> str:
        """Convert results to JSON string."""
        return self.json(**kwargs)
    
    def filter_services(self, **filters) -> List[NetworkService]:
        """Filter services based on provided criteria."""
        def matches(service: NetworkService) -> bool:
            for key, value in filters.items():
                if getattr(service, key, None) != value:
                    return False
            return True
            
        return [s for s in self.services if matches(s)]
    
    def get_service(self, port: int, protocol: Protocol = Protocol.TCP) -> Optional[NetworkService]:
        """Get service by port and protocol."""
        for service in self.services:
            if service.port == port and service.protocol == protocol:
                return service
        return None
