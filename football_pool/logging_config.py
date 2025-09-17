"""
Comprehensive logging configuration for Football Pool Domination System.

Provides detailed logging for:
- Command execution
- LLM interactions and API calls
- Prompt generation and responses
- Excel automation operations
- Error tracking and debugging
"""

import json
import logging
from datetime import datetime
from pathlib import Path


class FootballPoolLogger:
    """Centralized logging system for the football pool application."""

    def __init__(self, log_dir: str = "logs"):
        """Initialize the logging system."""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        # Create loggers for different components
        self.command_logger = self._setup_logger("commands", "command_execution.log")
        self.llm_logger = self._setup_logger("llm", "llm_interactions.log")
        self.excel_logger = self._setup_logger("excel", "excel_automation.log")
        self.api_logger = self._setup_logger("api", "api_calls.log")
        self.debug_logger = self._setup_logger("debug", "debug.log")

        # Main application logger
        self.app_logger = self._setup_logger("app", "football_pool.log")

    def _setup_logger(self, name: str, filename: str) -> logging.Logger:
        """Setup a logger with file and console handlers."""
        logger = logging.getLogger(f"football_pool.{name}")
        logger.setLevel(logging.DEBUG)

        # Clear existing handlers
        logger.handlers.clear()

        # File handler
        log_file = self.log_dir / filename
        file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        # Console handler (less verbose)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def log_command_start(self, command: str, args: dict = None):
        """Log the start of a command execution."""
        self.command_logger.info(f"🚀 Starting command: {command}")
        if args:
            self.command_logger.debug(f"Command arguments: {json.dumps(args, indent=2)}")

    def log_command_end(self, command: str, success: bool = True, duration: float = None):
        """Log the end of a command execution."""
        status = "✅ SUCCESS" if success else "❌ FAILED"
        duration_str = f" (took {duration:.2f}s)" if duration else ""
        self.command_logger.info(f"🏁 Command completed: {command} - {status}{duration_str}")

    def log_llm_request(self, model: str, prompt: str, context: dict = None):
        """Log LLM request details."""
        self.llm_logger.info(f"🤖 LLM Request to {model}")
        self.llm_logger.debug(f"Prompt length: {len(prompt)} characters")
        self.llm_logger.debug(f"Prompt preview: {prompt[:200]}...")
        if context:
            self.llm_logger.debug(f"Context: {json.dumps(context, indent=2)}")

    def log_llm_response(
        self, model: str, response: str, tokens_used: int = None, cost: float = None
    ):
        """Log LLM response details."""
        self.llm_logger.info(f"📝 LLM Response from {model}")
        self.llm_logger.debug(f"Response length: {len(response)} characters")
        if tokens_used:
            self.llm_logger.debug(f"Tokens used: {tokens_used}")
        if cost:
            self.llm_logger.debug(f"Cost: ${cost:.4f}")
        self.llm_logger.debug(f"Response preview: {response[:200]}...")

    def log_api_call(
        self,
        service: str,
        endpoint: str,
        method: str = "GET",
        status_code: int = None,
        response_time: float = None,
    ):
        """Log API call details."""
        status_str = f" (Status: {status_code})" if status_code else ""
        time_str = f" (took {response_time:.2f}s)" if response_time else ""
        self.api_logger.info(f"🌐 API Call: {method} {service}/{endpoint}{status_str}{time_str}")

    def log_excel_operation(self, operation: str, file_path: str, details: dict = None):
        """Log Excel automation operations."""
        self.excel_logger.info(f"📊 Excel Operation: {operation} on {file_path}")
        if details:
            self.excel_logger.debug(f"Details: {json.dumps(details, indent=2)}")

    def log_prompt_generation(self, prompt_type: str, date: str, games_count: int = None):
        """Log prompt generation details."""
        games_str = f" ({games_count} games)" if games_count else ""
        self.llm_logger.info(f"📝 Generated {prompt_type} prompt for {date}{games_str}")

    def log_error(self, error: Exception, context: str = None):
        """Log errors with context."""
        self.debug_logger.error(f"💥 Error: {str(error)}")
        if context:
            self.debug_logger.error(f"Context: {context}")
        self.debug_logger.exception("Full traceback:")

    def log_performance(self, operation: str, duration: float, details: dict = None):
        """Log performance metrics."""
        self.debug_logger.info(f"⏱️ Performance: {operation} took {duration:.2f}s")
        if details:
            self.debug_logger.debug(f"Performance details: {json.dumps(details, indent=2)}")

    def get_log_summary(self) -> dict:
        """Get a summary of recent log activity."""
        summary = {"log_directory": str(self.log_dir), "log_files": [], "total_size": 0}

        for log_file in self.log_dir.glob("*.log"):
            stat = log_file.stat()
            summary["log_files"].append(
                {
                    "name": log_file.name,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                }
            )
            summary["total_size"] += stat.st_size

        return summary


# Global logger instance
logger = FootballPoolLogger()


def get_logger(component: str = "app") -> logging.Logger:
    """Get a logger for a specific component."""
    return getattr(logger, f"{component}_logger", logger.app_logger)


def log_command(func):
    """Decorator to automatically log command execution."""

    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        command_name = func.__name__

        logger.log_command_start(command_name, kwargs)

        try:
            result = func(*args, **kwargs)
            duration = (datetime.now() - start_time).total_seconds()
            logger.log_command_end(command_name, success=True, duration=duration)
            return result
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.log_command_end(command_name, success=False, duration=duration)
            logger.log_error(e, f"Command: {command_name}")
            raise

    return wrapper
