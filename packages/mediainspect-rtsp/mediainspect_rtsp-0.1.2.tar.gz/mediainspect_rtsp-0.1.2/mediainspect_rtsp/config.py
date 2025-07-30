import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv
import logging
from pathlib import Path
import urllib.parse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class RTSPConfig:
    """RTSP configuration container"""
    user: str
    password: str
    host: str
    port: int
    path: str
    protocol: str
    timeout: int
    reconnect_attempts: int

    @property
    def url(self) -> str:
        """Generate RTSP URL with credentials"""
        # URL encode the username and password to handle special characters
        encoded_user = urllib.parse.quote(self.user)
        encoded_password = urllib.parse.quote(self.password)

        return f"rtsp://{encoded_user}:{encoded_password}@{self.host}:{self.port}{self.path}"

    @property
    def url_masked(self) -> str:
        """Generate RTSP URL with masked credentials for logging"""
        return f"rtsp://*****:*****@{self.host}:{self.port}{self.path}"


@dataclass
class ProcessingConfig:
    """Video processing configuration"""
    motion_threshold: float
    blur_size: int
    min_object_size: int
    max_object_size: int


class ConfigurationError(Exception):
    """Custom exception for configuration errors"""
    pass


class ConfigHandler:
    def __init__(self, env_path: Optional[str] = None):
        """
        Initialize configuration handler

        Args:
            env_path: Path to .env file (optional)
        """
        self.env_path = env_path or self._find_env_file()
        self._load_environment()

    def _find_env_file(self) -> str:
        """Find .env file in current or parent directories"""
        current_dir = Path.cwd()

        # Look in current and parent directories
        for directory in [current_dir, *current_dir.parents]:
            env_path = directory / '.env'
            if env_path.exists():
                return str(env_path)

        raise ConfigurationError("Could not find .env file")

    def _load_environment(self) -> None:
        """Load environment variables from .env file"""
        if not load_dotenv(self.env_path):
            raise ConfigurationError(f"Failed to load .env file from {self.env_path}")

        logger.info(f"Loaded configuration from {self.env_path}")

    def _get_env(self, key: str, default: Optional[str] = None, required: bool = True) -> str:
        """
        Get environment variable with validation

        Args:
            key: Environment variable key
            default: Default value if not found
            required: Whether the variable is required

        Returns:
            Environment variable value
        """
        value = os.getenv(key, default)
        if required and value is None:
            raise ConfigurationError(f"Required environment variable {key} not found")
        return value

    def get_rtsp_config(self) -> RTSPConfig:
        """Get RTSP configuration from environment"""
        try:
            return RTSPConfig(
                user=self._get_env('RTSP_USER'),
                password=self._get_env('RTSP_PASSWORD'),
                host=self._get_env('RTSP_HOST'),
                port=int(self._get_env('RTSP_PORT', '554')),
                path=self._get_env('RTSP_PATH', '/stream'),
                protocol=self._get_env('RTSP_PROTOCOL', 'tcp'),
                timeout=int(self._get_env('RTSP_TIMEOUT', '30')),
                reconnect_attempts=int(self._get_env('RTSP_RECONNECT_ATTEMPTS', '3'))
            )
        except ValueError as e:
            raise ConfigurationError(f"Invalid RTSP configuration: {str(e)}")

    def get_processing_config(self) -> ProcessingConfig:
        """Get processing configuration from environment"""
        try:
            return ProcessingConfig(
                motion_threshold=float(self._get_env('MOTION_THRESHOLD', '25.0')),
                blur_size=int(self._get_env('BLUR_SIZE', '21')),
                min_object_size=int(self._get_env('MIN_OBJECT_SIZE', '1000')),
                max_object_size=int(self._get_env('MAX_OBJECT_SIZE', '100000'))
            )
        except ValueError as e:
            raise ConfigurationError(f"Invalid processing configuration: {str(e)}")

    def validate_configuration(self) -> bool:
        """Validate all configuration settings"""
        try:
            rtsp_config = self.get_rtsp_config()
            processing_config = self.get_processing_config()

            # Validate RTSP configuration
            if not rtsp_config.host:
                raise ConfigurationError("RTSP host cannot be empty")
            if rtsp_config.port < 1 or rtsp_config.port > 65535:
                raise ConfigurationError("Invalid RTSP port number")
            if rtsp_config.protocol not in ['tcp', 'udp']:
                raise ConfigurationError("RTSP protocol must be 'tcp' or 'udp'")

            # Validate processing configuration
            if processing_config.motion_threshold < 0:
                raise ConfigurationError("Motion threshold cannot be negative")
            if processing_config.blur_size % 2 != 1:
                raise ConfigurationError("Blur size must be odd")
            if processing_config.min_object_size >= processing_config.max_object_size:
                raise ConfigurationError("Min object size must be less than max object size")

            logger.info("Configuration validation successful")
            logger.info(f"RTSP URL: {rtsp_config.url_masked}")

            return True

        except Exception as e:
            logger.error(f"Configuration validation failed: {str(e)}")
            return False