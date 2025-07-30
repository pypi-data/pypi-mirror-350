import argparse
import asyncio
import json
from .simple_network_scanner import SimpleNetworkScanner

async def main():
    parser = argparse.ArgumentParser(description="Network scanner for mediainspect.")
    parser.add_argument('--ip', required=True, help='IP address to scan')
    parser.add_argument('--port', type=int, nargs='+', required=True, help='Ports to scan')
    args = parser.parse_args()

    scanner = SimpleNetworkScanner()
    results = []
    for port in args.port:
        result = await scanner.scan_port(args.ip, port)
        results.append(result)
    print(json.dumps([r.__dict__ for r in results], indent=2))

if __name__ == "__main__":
    asyncio.run(main())
