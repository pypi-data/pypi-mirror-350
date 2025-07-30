"""
High-level network scanning interface.

This module provides a simplified interface for common network scanning tasks,
built on top of the lower-level scanner_worker.
"""
import asyncio
import logging
from typing import List, Dict, Any, Optional, Set, Union
from dataclasses import dataclass
from datetime import datetime

from .models import NetworkService, Protocol, ServiceStatus, ScanResult
from .scanner_worker import ScannerWorker, ScanTask

logger = logging.getLogger(__name__)

# Common ports for well-known services
COMMON_PORTS = {
    'rtsp': [554, 8554, 1935, 1936],
    'http': [80, 8080, 8000, 8888],
    'https': [443, 8443],
    'ssh': [22],
    'vnc': [5900, 5901],
    'rdp': [3389],
    'mqtt': [1883],
    'mqtts': [8883],
    'rtmp': [1935],
    'rtsp-tls': [322],
    'sip': [5060, 5061],
    'sip-tls': [5061],
    'onvif': [3702],
    'rtsp-over-http': [80, 8000, 8080, 8081, 8888],
    'rtsp-over-https': [443, 8443],
}

# Reverse mapping for port to service name
PORT_TO_SERVICE = {
    port: service
    for service, ports in COMMON_PORTS.items()
    for port in ports
}


class SimpleNetworkScanner:
    """
    High-level network scanner with common port scanning capabilities.
    
    This class provides a simple interface for common scanning tasks while
    handling connection pooling, rate limiting, and concurrency internally.
    """
    
    def __init__(
        self,
        max_concurrent: int = 100,
        request_timeout: float = 2.0,
        rate_limit: int = 1000,
    ):
        """
        Initialize the scanner.
        
        Args:
            max_concurrent: Maximum number of concurrent connections
            request_timeout: Default timeout for network requests
            rate_limit: Maximum requests per second
        """
        self.max_concurrent = max_concurrent
        self.request_timeout = request_timeout
        self.rate_limit = rate_limit
        self._worker = None
    
    async def _get_worker(self) -> ScannerWorker:
        """Get or create a scanner worker."""
        if self._worker is None:
            self._worker = ScannerWorker(
                max_concurrent=self.max_concurrent,
                request_timeout=self.request_timeout,
                rate_limit=self.rate_limit
            )
        return self._worker
    
    async def scan_port(
        self,
        ip: str,
        port: int,
        protocol: Protocol = Protocol.TCP,
    ) -> NetworkService:
        """
        Scan a single port.
        
        Args:
            ip: Target IP address or hostname
            port: Port number to scan
            protocol: Network protocol (TCP/UDP)
            
        Returns:
            NetworkService with scan results
        """
        worker = await self._get_worker()
        service = await worker.scan_port(ip, port, protocol)
        
        # Set service name based on common ports
        if service.status == ServiceStatus.UP and service.service == 'unknown':
            service.service = PORT_TO_SERVICE.get(port, 'unknown')
            
        return service
        
        return models.NetworkService(
            ip=ip,
            port=port,
            service=service_info['service'],
            protocol=service_info['protocol'],
            banner=service_info['banner'],
            is_secure=service_info['secure'],
            is_up=True
        )
    
    async def scan_ports(self, ip: str, ports: List[int]) -> models.ScanResult:
        """
        Scan multiple ports concurrently.
        
        Args:
            ip: IP address to scan
            ports: List of port numbers to scan
            
        Returns:
            ScanResult object with scan results
        """
        start_time = time.monotonic()
        tasks = [self.scan_port(ip, port) for port in ports]
        services = await asyncio.gather(*tasks, return_exceptions=False)
        duration = time.monotonic() - start_time
        
        return models.ScanResult(
            services=services,
            duration=duration
        )
    
    async def scan_common_ports(self, ip: str) -> models.ScanResult:
        """
        Scan all common ports for a given IP.
        
        Args:
            ip: IP address to scan
            
        Returns:
            ScanResult object with scan results
        """
        # Flatten the list of common ports
        ports = [port for port_list in self.COMMON_PORTS.values() for port in port_list]
        return await self.scan_ports(ip, ports)
