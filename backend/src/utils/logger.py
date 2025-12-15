"""
Structured logging configuration for the application.

This module provides a configured logger with JSON formatting for
structured logging suitable for monitoring and debugging.
"""

import logging
import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    """Custom formatter that outputs logs in JSON format."""
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON.
        
        Args:
            record: LogRecord instance to format
            
        Returns:
            JSON string with log information
        """
        log_data: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception information if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields from LogRecord
        if hasattr(record, 'extra'):
            log_data["context"] = record.extra
        
        # Include any additional attributes added via extra parameter
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'created', 'filename', 'funcName',
                          'levelname', 'levelno', 'lineno', 'module', 'msecs',
                          'message', 'pathname', 'process', 'processName',
                          'relativeCreated', 'thread', 'threadName', 'exc_info',
                          'exc_text', 'stack_info', 'extra']:
                if not key.startswith('_'):
                    if 'context' not in log_data:
                        log_data['context'] = {}
                    log_data['context'][key] = value
        
        return json.dumps(log_data, default=str)


def setup_logger(
    name: str = "global_news_brief",
    level: int = logging.INFO,
    json_format: bool = True
) -> logging.Logger:
    """
    Configure and return a logger instance.
    
    Args:
        name: Logger name (default: "global_news_brief")
        level: Logging level (default: INFO)
        json_format: Use JSON formatter if True, standard formatter if False
        
    Returns:
        Configured logger instance
        
    Example:
        logger = setup_logger("my_module", level=logging.DEBUG)
        logger.info("Application started", extra={"version": "1.0"})
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Set formatter
    if json_format:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%SZ'
        )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger


# Create default logger instance
logger = setup_logger()


def log_execution(func):
    """
    Decorator to log function execution with timing.
    
    Example:
        @log_execution
        def fetch_news():
            return api.get('/news')
    """
    from functools import wraps
    import time
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_logger = logging.getLogger(func.__module__)
        start_time = time.time()
        
        func_logger.info(
            f"Starting execution of {func.__name__}",
            extra={
                "function": func.__name__,
                "module": func.__module__
            }
        )
        
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            
            func_logger.info(
                f"Completed {func.__name__} in {duration:.2f}s",
                extra={
                    "function": func.__name__,
                    "duration_seconds": round(duration, 2),
                    "status": "success"
                }
            )
            
            return result
        except Exception as e:
            duration = time.time() - start_time
            
            func_logger.error(
                f"Failed {func.__name__} after {duration:.2f}s: {str(e)}",
                extra={
                    "function": func.__name__,
                    "duration_seconds": round(duration, 2),
                    "status": "error",
                    "error": str(e)
                },
                exc_info=True
            )
            raise
    
    return wrapper
