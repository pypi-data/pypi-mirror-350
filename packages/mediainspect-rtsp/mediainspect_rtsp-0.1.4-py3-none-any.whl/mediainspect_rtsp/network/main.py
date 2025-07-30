"""
Command-line interface for network scanning.
"""
import asyncio
import argparse
from typing import List, Optional

from .scanner import SimpleNetworkScanner
from . import utils


async def main(args: Optional[List[str]] = None) -> None:
    """Main entry point for the network scanner CLI."""
    parser = argparse.ArgumentParser(description='Network scanner for mediainspect')
    parser.add_argument('ip', help='IP address or hostname to scan')
    parser.add_argument('-p', '--ports', help='Ports to scan (comma-separated or range)')
    parser.add_argument('-c', '--common', action='store_true', help='Scan common ports')
    parser.add_argument('-t', '--timeout', type=float, default=2.0, help='Connection timeout in seconds')
    
    # Parse command line arguments
    parsed_args = parser.parse_args(args)
    
    if not parsed_args.ports and not parsed_args.common:
        print("Error: You must specify either --ports or --common")
        return
    
    scanner = SimpleNetworkScanner(timeout=parsed_args.timeout)
    
    try:
        if parsed_args.common:
            print(f"Scanning common ports on {parsed_args.ip}...")
            results = await scanner.scan_common_ports(parsed_args.ip)
        else:
            ports = utils.parse_ports(parsed_args.ports)
            print(f"Scanning ports {ports} on {parsed_args.ip}...")
            results = await scanner.scan_ports(parsed_args.ip, ports)
        
        # Print formatted results
        print(utils.format_scan_results(results))
        
    except KeyboardInterrupt:
        print("\nScan aborted by user")
    except Exception as e:
        print(f"\nError: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
