import sys
import uuid
import loguru
from .ConfigSettings import settings


class CustomLogging:
    """
    Handles custom logging operations for the application.

    This class provides a centralized logging mechanism using the `loguru` library. It is designed
    to configure logging settings based on application-specific configurations, including app name,
    log levels, and message formats. It dynamically sets up a logger instance and ensures each
    log entry includes contextual information such as a unique request identifier, app name, and
    API key.

    :ivar _app_name: Name of the application used for log context.
    :type _app_name: str
    :ivar _log_level: Logging level such as DEBUG, INFO, WARNING, etc., for customization.
    :type _log_level: str
    :ivar _log_message_format: Format string for log messages to customize the logging output.
    :type _log_message_format: str
    :ivar _api_key: Default API key format used in logging for operational context.
    :type _api_key: str
    :ivar _logger: Configured `loguru` logger instance for logging messages.
    :type _logger: loguru.Logger
    """
    DEFAULT_LOG_FORMAT = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {extra[app]} | "
        "<blue>{extra[request_id]}</blue> | <green>{extra[key]}</green> | "
        "<level>{level: <8}</level> | <cyan><level>{message}</level></cyan>")
    DEFAULT_API_KEY = f'{"":->12}'

    def __init__(self):
        self._app_name = getattr(settings, "LOG_APPNAME", "DefaultAppName")
        self._log_level = getattr(settings, "LOG_LEVEL", "INFO")
        self._log_message_format = getattr(settings, "LOG_FORMAT", self.DEFAULT_LOG_FORMAT)
        self._api_key = self.DEFAULT_API_KEY

        self._logger = self._initialize_logger()

    def _initialize_logger(self):
        """Configure and return the initialized logger instance."""
        loguru_config = {
            "handlers": [
                {"sink": sys.stdout, "format": self._log_message_format, "level": self._log_level},
            ],
            "extra": {"app": self._app_name, "request_id": self._request_id, "key": self._api_key},
        }
        loguru.logger.remove()
        loguru.logger.configure(**loguru_config)
        return loguru.logger

    @property
    def _request_id(self):
        """Dynamically generate a unique request ID."""
        return str(uuid.uuid4())

    @property
    def logger(self):
        return self._logger

# Usage
logger = CustomLogging().logger
