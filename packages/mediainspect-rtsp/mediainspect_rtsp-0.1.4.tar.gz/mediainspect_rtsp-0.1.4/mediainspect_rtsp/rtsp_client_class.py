from .config_handler import ConfigHandler
import logging

logger = logging.getLogger(__name__)

class RTSPClient:
    def __init__(self, config_path: str = None):
        try:
            self.config_handler = ConfigHandler(config_path)
            if not self.config_handler.validate_configuration():
                raise Exception("Configuration validation failed")
            self.rtsp_config = self.config_handler.get_rtsp_config()
            self.processing_config = self.config_handler.get_processing_config()
            self.cap = None
        except Exception as e:
            logger.error(f"Failed to initialize RTSP client: {str(e)}")
            raise
