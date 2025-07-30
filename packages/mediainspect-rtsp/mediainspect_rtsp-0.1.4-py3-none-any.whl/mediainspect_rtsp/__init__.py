"""
mediainspect-rtsp - RTSP and network inspection tools.

This package provides tools for working with RTSP streams and network scanning.
"""
import warnings

# Import network scanning functionality
from .network import (
    NetworkService,
    ScanResult,
    SimpleNetworkScanner,
    parse_ports,
    format_scan_results
)

__all__ = [
    'NetworkService',
    'ScanResult',
    'SimpleNetworkScanner',
    'parse_ports',
    'format_scan_results'
]

# Deprecation notice
warnings.warn(
    "The 'simple_network_scanner' and 'network_scanner' modules are deprecated. "
    "Please use 'mediainspect_rtsp.network' instead.",
    DeprecationWarning,
    stacklevel=2
)
