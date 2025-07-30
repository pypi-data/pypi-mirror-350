import asyncio
from typing import List, Optional, Dict, Any
from .network_service import NetworkService

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
