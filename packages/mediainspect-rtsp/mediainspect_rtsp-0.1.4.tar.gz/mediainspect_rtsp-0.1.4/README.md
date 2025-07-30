# RTSP Stream Processor

Real-time RTSP video stream processor with motion detection, object recognition, and analysis capabilities. Built with Python and OpenCV.

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/mediainspect/rtsp/actions)
[![PyPI version](https://badge.fury.io/py/mediainspect-rtsp.svg)](https://badge.fury.io/py/mediainspect-rtsp)
[![License](https://img.shields.io/github/license/mediainspect/rtsp.svg)](https://github.com/mediainspect/rtsp/blob/main/LICENSE)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Coverage Status](https://coveralls.io/repos/github/mediainspect/rtsp/badge.svg?branch=main)](https://coveralls.io/github/mediainspect/rtsp?branch=main)

## Author
Tom Sapletta

## Repository
https://github.com/mediainspect/rtsp.git

## 🚀 Features

- **RTSP Stream Handling**
  - Secure credential management
  - Automatic reconnection
  - Buffer management
  - Support for TCP/UDP protocols

- **Network Scanning**
  - Port scanning without root privileges
  - Service identification
  - Common port detection
  - Concurrent scanning
  - Banner grabbing

- **Video Processing**
  - Motion detection
  - Object recognition
  - Frame analysis
  - Real-time statistics

- **Monitoring**
  - Performance metrics
  - Health checks
  - Processing statistics
  - Docker integration

## 🌟 Network Scanning

The `mediainspect_rtsp.network` package provides powerful network scanning capabilities without requiring root privileges.

### Key Components

- `SimpleNetworkScanner`: Main scanner class for port and service detection
- `NetworkService`: Dataclass representing a discovered network service
- `ScanResult`: Container for scan results with metadata

### Basic Usage

```python
import asyncio
from mediainspect_rtsp.network import SimpleNetworkScanner, format_scan_results

async def main():
    # Create a scanner instance
    scanner = SimpleNetworkScanner(timeout=2.0)
    
    # Scan common ports on a host
    results = await scanner.scan_common_ports("example.com")
    print(format_scan_results(results))
    
    # Or scan specific ports
    results = await scanner.scan_ports("example.com", [80, 443, 8080])
    print(f"Found {len(results.services)} services")

# Run the async function
asyncio.run(main())
```

### Command Line Interface

```bash
# Scan common ports on a host
python -m mediainspect_rtsp.network.main example.com --common

# Scan specific ports
python -m mediainspect_rtsp.network.main example.com --ports 80,443,8080-8090

# With custom timeout
python -m mediainspect_rtsp.network.main example.com --common --timeout 1.5
```

### API Reference

#### `SimpleNetworkScanner`

- `__init__(self, timeout: float = 2.0)`: Initialize with connection timeout
- `scan_port(ip: str, port: int) -> NetworkService`: Scan a single port
- `scan_ports(ip: str, ports: List[int]) -> ScanResult`: Scan multiple ports concurrently
- `scan_common_ports(ip: str) -> ScanResult`: Scan all common ports
- `check_port(ip: str, port: int) -> bool`: Check if a port is open
- `identify_service(ip: str, port: int) -> Dict[str, Any]`: Identify service on a port

#### `NetworkService`

- `ip: str`: IP address of the service
- `port: int`: Port number
- `service: str`: Service name (e.g., 'http', 'ssh')
- `protocol: str`: Protocol (usually 'tcp' or 'udp')
- `banner: str`: Service banner if available
- `is_secure: bool`: Whether the connection is secure
- `is_up: bool`: Whether the service is up

#### `ScanResult`

- `services: List[NetworkService]`: List of discovered services
- `duration: float`: Scan duration in seconds
- `total_ports: int`: Total number of ports scanned
- `open_ports: int`: Number of open ports found
- `to_dict() -> Dict`: Convert results to dictionary

#### Utility Functions

- `parse_ports(ports_str: str) -> List[int]`: Parse port string (e.g., "80,443,8080-8090")
- `format_scan_results(results: ScanResult) -> str`: Format results as a string

### Advanced Examples

#### Example 1: Network Inventory

Create an inventory of all services running on common ports across multiple hosts:

```python
import asyncio
from mediainspect_rtsp.network import SimpleNetworkScanner

async def scan_hosts(hosts):
    scanner = SimpleNetworkScanner()
    tasks = [scanner.scan_common_ports(host) for host in hosts]
    return await asyncio.gather(*tasks)

hosts = ["192.168.1.1", "192.168.1.100", "192.168.1.200"]
results = asyncio.run(scan_hosts(hosts))

for host, result in zip(hosts, results):
    print(f"\n{host} - {result.open_ports} open ports:")
    for service in result.services:
        if service.is_up:
            print(f"  - {service.port}/tcp: {service.service}")
```

#### Example 2: Security Check for Common Vulnerable Services

Check for potentially vulnerable services that should be secured:

```python
import asyncio
from mediainspect_rtsp.network import SimpleNetworkScanner

VULNERABLE_SERVICES = {
    'ftp': 21,
    'telnet': 23,
    'http': 80,
    'snmp': 161,
    'mssql': 1433,
    'oracle': 1521,
    'mysql': 3306,
    'rdp': 3389,
    'vnc': [5900, 5901]
}

async def check_vulnerable_services(host):
    scanner = SimpleNetworkScanner()
    ports = []
    
    # Get all ports from vulnerable services
    for service in VULNERABLE_SERVICES.values():
        if isinstance(service, list):
            ports.extend(service)
        else:
            ports.append(service)
            
    results = await scanner.scan_ports(host, ports)
    
    print(f"\nSecurity check for {host}:")
    for service in results.services:
        if service.is_up:
            status = "⚠️  WARNING" if service.port in [21, 23, 161] else "ℹ️  INFO"
            print(f"{status} - {service.port}/tcp: {service.service} is running")
            if service.banner:
                print(f"     Banner: {service.banner[:100]}...")

# Run the check
asyncio.run(check_vulnerable_services("example.com"))
```

#### Example 3: Monitor Service Availability

Continuously monitor services and alert on status changes:

```python
import asyncio
import time
from datetime import datetime
from mediainspect_rtsp.network import SimpleNetworkScanner

class ServiceMonitor:
    def __init__(self, host, ports, interval=300):
        self.host = host
        self.ports = ports
        self.interval = interval
        self.scanner = SimpleNetworkScanner()
        self.known_services = {}
    
    async def check_services(self):
        results = await self.scanner.scan_ports(self.host, self.ports)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Check for new services
        for service in results.services:
            port_key = f"{service.port}/{service.protocol}"
            
            if service.is_up and port_key not in self.known_services:
                print(f"[{current_time}] NEW SERVICE: {port_key} - {service.service}")
                self.known_services[port_key] = service
            elif not service.is_up and port_key in self.known_services:
                print(f"[{current_time}] SERVICE DOWN: {port_key} - {self.known_services[port_key].service}")
                del self.known_services[port_key]
    
    async def run(self):
        print(f"Starting service monitor for {self.host}...")
        while True:
            try:
                await self.check_services()
                await asyncio.sleep(self.interval)
            except KeyboardInterrupt:
                print("\nStopping monitor...")
                break
            except Exception as e:
                print(f"Error during scan: {e}")
                await asyncio.sleep(5)

# Monitor common services
monitor = ServiceMonitor(
    host="example.com",
    ports=[21, 22, 23, 25, 53, 80, 443, 3306, 3389, 5432, 8080, 8443],
    interval=300  # 5 minutes
)
asyncio.run(monitor.run())
```

#### Example 4: Find RTSP Cameras on Local Network

Scan for RTSP cameras on the local network:

```python
import asyncio
import ipaddress
from mediainspect_rtsp.network import SimpleNetworkScanner

RTSP_PORTS = [554, 8554, 1935, 1936, 8080, 8081, 8082, 8888, 1935]

def get_local_ips():
    """Get all IPs in local network"""
    # This is a simplified example - you might want to use a more robust method
    network = ipaddress.IPv4Network("192.168.1.0/24", strict=False)
    return [str(ip) for ip in network.hosts()]

async def find_rtsp_cameras():
    scanner = SimpleNetworkScanner(timeout=1.0)
    local_ips = get_local_ips()
    
    print(f"Scanning {len(local_ips)} IPs for RTSP cameras...")
    
    for ip in local_ips:
        try:
            results = await scanner.scan_ports(ip, RTSP_PORTS)
            for service in results.services:
                if service.is_up and service.service == 'rtsp':
                    print(f"\n🎥 Found RTSP camera at rtsp://{ip}:{service.port}")
                    if service.banner:
                        print(f"   Banner: {service.banner}")
        except Exception as e:
            print(f"Error scanning {ip}: {e}")

asyncio.run(find_rtsp_cameras())
```

### Best Practices

1. **Rate Limiting**:
   - Add delays between scans to avoid overwhelming networks
   - Use `asyncio.sleep()` between batches of scans

2. **Error Handling**:
   - Always wrap scans in try/except blocks
   - Handle common exceptions like `ConnectionRefusedError`, `TimeoutError`

3. **Performance**:
   - Adjust the `timeout` parameter based on network conditions
   - For large scans, process results in batches

4. **Security**:
   - Only scan networks you have permission to scan
   - Be aware of legal implications in your jurisdiction
   - Consider adding authentication when accessing services

## 📋 Prerequisites

- Python 3.7+
- FFmpeg
- OpenCV dependencies
- Docker (optional)



## 🛠️ Makefile Usage

The Makefile provides convenient commands for common tasks. Run `make help` to see all available targets.

### Project Management

- `make install`        – Install dependencies
- `make test`           – Run tests
- `make lint`           – Lint code
- `make run`            – Run the main application
- `make clean`          – Remove caches

### Network Scanning

- `make scan-network`   – Scan the default network for common services
- `make scan-cameras`   – Scan for cameras and related services
- `make scan-camera IP=192.168.1.100` – Scan a specific camera IP
- `make scan-quick`     – Quick scan of common ports
- `make scan-full`      – Comprehensive scan
- `make scan-local`     – Scan common local network ranges

### Printer Management

- `make scan-printers`  – List all available printers

### Shell & Interactive Clients

- `make shell`          – Start a Python shell in the package context (now in `scripts/`)
- `make interactive`    – Start the interactive command-line client (now in `scripts/`)

### Help

- `make help`           – Show all available targets

## 🐚 Shell Client

Start an interactive Python shell with project context:

```bash
make shell
```

(Uses `scripts/shell_client.py`)

## 🖥️ Interactive CLI

Launch the interactive command-line interface:

```bash
make interactive
```

(Uses `scripts/interactive_client.py`)

## 🔍 Network Scanning & Printing

mediainspect includes powerful network scanning capabilities to discover devices like cameras and printers on your local network.

### Scan for Network Devices

Scan your local network for various devices and services:

```bash
make scan-network
```

### Discover Cameras

Find RTSP cameras on your network:

```bash
make scan-cameras
```


### Print a Test Page

Send a test page to your default printer:

```bash
make print-test
```

### Using the Network Scanner in Python

You can also use the network scanner directly in your Python code:

```python
from mediainspect.scanner import NetworkScanner
import asyncio

async def scan_network():
    scanner = NetworkScanner()
    
    # Scan for all services
    services = await scanner.scan_network()
    
    # Or scan for specific service types
    cameras = await scanner.scan_network(service_types=['rtsp'])
    
    for service in services:
        print(f"{service.ip}:{service.port} - {service.service} ({service.banner})")

# Run the scan
asyncio.run(scan_network())
```

## 🖨️ Printing Support

mediainspect includes basic printing capabilities using the CUPS (Common Unix Printing System) interface.



## 🔧 Installation

### Using pip

```bash
# Clone the repository
git clone https://github.com/mediainspect/rtsp.git
cd rtsp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

start
```bash
python main.py
```

### Using Docker

```bash
# Build and run using docker-compose
docker-compose up -d

# View logs
docker-compose logs -f
```

## ⚙️ Configuration

1. Create environment file:
```bash
cp .env.template .env
```

2. Configure your settings:
```env
# RTSP Credentials
RTSP_USER=your_username
RTSP_PASSWORD=your_password

# RTSP Stream Configuration
RTSP_HOST=stream_host_ip
RTSP_PORT=554
RTSP_PATH=/stream

# Processing Configuration
MOTION_THRESHOLD=25.0
BLUR_SIZE=21
```

## 💻 Usage

### Basic Usage

```python
from rtsp_client import RTSPClient

# Initialize client
client = RTSPClient()

# Connect to stream
if client.connect():
    try:
        while True:
            frame = client.read_frame()
            # Process frame here
    finally:
        client.disconnect()
```

### With Custom Processing

```python
from video_processor import VideoProcessor

processor = VideoProcessor(
    motion_threshold=25.0,
    blur_size=21,
    min_object_size=1000
)

def process_frame(frame):
    processed_frame, stats = processor.process(frame)
    return processed_frame
```

## 📦 Python Package Information

- **Package name:** mediainspect-rtsp
- **PyPI:** https://pypi.org/project/mediainspect-rtsp/
- **Source:** https://github.com/mediainspect/rtsp
- **License:** Apache 2.0
- **Author:** Tom Sapletta
- **Description:** Real-time RTSP video stream processor with motion detection, object recognition, and analysis capabilities. Built with Python and OpenCV.

### Installation

```bash
pip install mediainspect-rtsp
```

### Usage Example

```python
from mediainspect_rtsp.video_processor_rtsp_class import VideoProcessor

processor = VideoProcessor(rtsp_url="rtsp://...", motion_threshold=25.0)
processor.run()
```

For more details, see the [PyPI page](https://pypi.org/project/mediainspect-rtsp/) and [documentation](https://github.com/mediainspect/rtsp).

## 🔍 Monitor and Debug

### Health Checks

Access health metrics at:
- http://localhost:8080/health
- http://localhost:8080/metrics

### Prometheus & Grafana

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## 🛠️ Development

### Project Structure

```
rtsp-processor/
├── src/
│   ├── rtsp_client.py     # RTSP handling
│   ├── video_processor.py # Video processing
│   └── config.py         # Configuration management
├── tests/
│   └── test_*.py        # Test files
├── docker/
│   ├── Dockerfile       # Container definition
│   └── docker-compose.yml
├── .env.template        # Environment template
├── scripts/
│   ├── shell_client.py  # Shell client
│   └── interactive_client.py  # Interactive client
└── README.md           # This file
```

## 🧪 Running Tests

This project uses pytest for testing. To run all tests:

```bash
make test
```

Or directly with pytest:

```bash
pytest
```

All modules in `mediainspect_rtsp/` are covered by basic import tests in `tests/`. Extend these with functional tests as needed.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 Versioning

We use [SemVer](http://semver.org/) for versioning. For available versions, see the [CHANGELOG.md](CHANGELOG.md).

## 🔒 Security

### Credential Handling

- Credentials stored in .env file
- Passwords never logged
- URL encoding for special characters
- Secure connection handling

### Best Practices

- Use environment variables
- Regularly update dependencies
- Follow security advisories
- Implement proper error handling

## ❗ Common Issues

1. **OpenCV Import Error**
```bash
# Install system dependencies
sudo ./install_opencv.sh
```

2. **RTSP Connection Failed**
- Verify credentials
- Check network connectivity
- Confirm stream availability

3. **Performance Issues**
- Adjust buffer size
- Modify processing parameters
- Check system resources

## 📈 Performance Tuning

### Memory Usage

```python
# Configure buffer size
client = RTSPClient(buffer_size=1024*1024)
```

### Processing Speed

```python
# Adjust processing parameters
processor = VideoProcessor(
    skip_frames=2,
    downscale_factor=0.5
)
```

## 📚 Documentation

- [API Reference](docs/API.md)
- [Configuration Guide](docs/CONFIGURATION.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- OpenCV community
- FFmpeg project
- Docker community
- All contributors

## 📞 Support

For support, please:
1. Check documentation
2. Search existing issues
3. Create new issue if needed

## 🔄 Changelog

See [CHANGELOG.md](CHANGELOG.md) for all changes.