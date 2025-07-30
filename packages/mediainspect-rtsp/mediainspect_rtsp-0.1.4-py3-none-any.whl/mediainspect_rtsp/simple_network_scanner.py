import asyncio
from typing import List, Optional, Dict, Any, Set
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

class SimpleNetworkScanner:
    """Simple network scanner that doesn't require root privileges."""
    
    COMMON_PORTS = {
        'rtsp': [554, 8554],
        'http': [80, 8080, 8000, 8888],
        'https': [443, 8443],
        'ssh': [22],
        'vnc': [5900, 5901],
        'rdp': [3389],
        'mqtt': [1883],
        'mqtts': [8883]
    }
    
    def __init__(self, timeout: float = 2.0):
        self.timeout = timeout
    
    async def check_port(self, ip: str, port: int) -> bool:
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, port),
                timeout=self.timeout
            )
            writer.close()
            await writer.wait_closed()
            return True
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError, ConnectionResetError):
            return False
    
    async def identify_service(self, ip: str, port: int) -> Dict[str, Any]:
        for service, ports in self.COMMON_PORTS.items():
            if port in ports:
                return {'service': service, 'protocol': 'tcp'}
        return {'service': 'unknown', 'protocol': 'tcp'}
    
    async def scan_port(self, ip: str, port: int) -> NetworkService:
        is_open = await self.check_port(ip, port)
        if not is_open:
            return NetworkService(ip=ip, port=port, is_up=False)
        service_info = await self.identify_service(ip, port)
        return NetworkService(
            ip=ip,
            port=port,
            service=service_info['service'],
            protocol=service_info['protocol'],
            banner=service_info.get('banner', ''),
            is_secure=service_info.get('secure', False),
            is_up=True
        )


def parse_ports(ports_str: str) -> List[int]:
    """
    Parse a string of ports into a list of integers.
    
    Args:
        ports_str: Comma-separated list of ports or port ranges (e.g., "80,443,8000-8002")
        
    Returns:
        List of unique, sorted port numbers
    """
    ports: Set[int] = set()
    
    for part in ports_str.split(','):
        part = part.strip()
        if not part:
            continue
            
        if '-' in part:
            # Handle port range (e.g., "8000-8002")
            try:
                start, end = map(int, part.split('-'))
                ports.update(range(start, end + 1))
            except (ValueError, IndexError):
                continue
        else:
            # Handle single port
            try:
                ports.add(int(part))
            except ValueError:
                continue
    
    return sorted(ports)


__all__ = [
    'SimpleNetworkScanner',
    'NetworkService',
    'parse_ports'
]
