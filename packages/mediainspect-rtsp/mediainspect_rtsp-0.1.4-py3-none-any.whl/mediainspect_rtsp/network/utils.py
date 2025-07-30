"""
Utility functions for network scanning.
"""
from typing import List, Set


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


def format_scan_results(results) -> str:
    """Format scan results as a human-readable string."""
    if not results.services:
        return "No results to display."
    
    output = []
    output.append(f"Scan completed in {results.duration:.2f} seconds")
    output.append(f"Scanned {results.total_ports} ports, {results.open_ports} open")
    output.append("\nOpen ports:")
    output.append("-" * 50)
    
    for service in results.services:
        if service.is_up:
            secure = " (secure)" if service.is_secure else ""
            banner = f" - {service.banner}" if service.banner else ""
            output.append(f"{service.ip}:{service.port} - {service.service.upper()}{secure}{banner}")
    
    return "\n".join(output)
