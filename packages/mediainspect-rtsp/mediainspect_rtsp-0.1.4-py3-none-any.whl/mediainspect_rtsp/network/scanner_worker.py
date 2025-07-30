"""
Core scanner worker implementation for concurrent network scanning.
"""
import asyncio
import logging
from typing import Dict, List, Optional, Set, Tuple, Any, Callable, Awaitable
from dataclasses import dataclass, field
from datetime import datetime

from .models import NetworkService, Protocol, ServiceStatus

logger = logging.getLogger(__name__)


@dataclass
class ScanTask:
    """Represents a single scan task."""
    ip: str
    port: int
    protocol: Protocol = Protocol.TCP
    timeout: float = 2.0
    callback: Optional[Callable[[NetworkService], Awaitable[None]]] = None


class ScannerWorker:
    """
    Handles concurrent network scanning with rate limiting and connection pooling.
    """
    
    def __init__(
        self,
        max_concurrent: int = 100,
        request_timeout: float = 2.0,
        rate_limit: int = 1000,  # Max requests per second
    ):
        """
        Initialize the scanner worker.
        
        Args:
            max_concurrent: Maximum number of concurrent connections
            request_timeout: Default timeout for network requests
            rate_limit: Maximum requests per second
        """
        self.max_concurrent = max_concurrent
        self.request_timeout = request_timeout
        self.rate_limit = rate_limit
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.active_tasks: Set[asyncio.Task] = set()
        
    async def _check_port(self, ip: str, port: int, protocol: Protocol) -> bool:
        """Check if a port is open."""
        try:
            _, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, port, proto=protocol.value),
                timeout=self.request_timeout
            )
            writer.close()
            await writer.wait_closed()
            return True
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError, ConnectionResetError) as e:
            logger.debug(f"Port check failed for {ip}:{port}/{protocol}: {e}")
            return False
    
    async def _identify_service(self, ip: str, port: int, protocol: Protocol) -> Dict[str, Any]:
        """Identify service running on the port."""
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, port, proto=protocol.value),
                timeout=self.request_timeout
            )
            
            # Try to read banner if possible
            banner = ""
            try:
                data = await asyncio.wait_for(reader.read(1024), timeout=1.0)
                banner = data.decode('utf-8', errors='ignore').strip()
            except (asyncio.TimeoutError, UnicodeDecodeError):
                pass
                
            writer.close()
            await writer.wait_closed()
            
            return {
                'banner': banner,
                'is_secure': port in {443, 993, 995, 465, 587, 990, 5061, 636, 563, 614},
                'status': ServiceStatus.UP
            }
            
        except Exception as e:
            logger.debug(f"Service identification failed for {ip}:{port}/{protocol}: {e}")
            return {
                'banner': '',
                'is_secure': False,
                'status': ServiceStatus.DOWN
            }
    
    async def _process_scan_task(self, task: ScanTask) -> NetworkService:
        """Process a single scan task."""
        async with self.semaphore:
            is_open = await self._check_port(task.ip, task.port, task.protocol)
            
            if not is_open:
                return NetworkService(
                    ip=task.ip,
                    port=task.port,
                    protocol=task.protocol,
                    status=ServiceStatus.DOWN
                )
            
            # If port is open, try to identify the service
            service_info = await self._identify_service(task.ip, task.port, task.protocol)
            
            return NetworkService(
                ip=task.ip,
                port=task.port,
                protocol=task.protocol,
                status=service_info['status'],
                banner=service_info['banner'],
                is_secure=service_info['is_secure'],
                metadata={
                    'scanned_at': datetime.utcnow().isoformat(),
                    'protocol': task.protocol.value
                }
            )
    
    async def scan_port(self, ip: str, port: int, protocol: Protocol = Protocol.TCP) -> NetworkService:
        """
        Scan a single port.
        
        Args:
            ip: Target IP address
            port: Port number to scan
            protocol: Network protocol (TCP/UDP)
            
        Returns:
            NetworkService with scan results
        """
        task = ScanTask(ip=ip, port=port, protocol=protocol)
        return await self._process_scan_task(task)
    
    async def scan_ports(
        self,
        ip: str,
        ports: List[int],
        protocol: Protocol = Protocol.TCP
    ) -> List[NetworkService]:
        """
        Scan multiple ports concurrently.
        
        Args:
            ip: Target IP address
            ports: List of port numbers to scan
            protocol: Network protocol (TCP/UDP)
            
        Returns:
            List of NetworkService objects with scan results
        """
        tasks = [self.scan_port(ip, port, protocol) for port in ports]
        return await asyncio.gather(*tasks, return_exceptions=False)
    
    async def scan_port_range(
        self,
        ip: str,
        start_port: int,
        end_port: int,
        protocol: Protocol = Protocol.TCP
    ) -> List[NetworkService]:
        """
        Scan a range of ports.
        
        Args:
            ip: Target IP address
            start_port: First port in range (inclusive)
            end_port: Last port in range (inclusive)
            protocol: Network protocol (TCP/UDP)
            
        Returns:
            List of NetworkService objects with scan results
        """
        ports = list(range(start_port, end_port + 1))
        return await self.scan_ports(ip, ports, protocol)
    
    async def close(self):
        """Clean up resources."""
        # Cancel any pending tasks
        for task in self.active_tasks:
            if not task.done():
                task.cancel()
        
        # Wait for all tasks to complete or be cancelled
        if self.active_tasks:
            await asyncio.wait(self.active_tasks)
        
        self.active_tasks.clear()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
