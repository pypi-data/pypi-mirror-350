import logging

# === Custom SUCCESS Log Level ===
SUCCESS_LEVEL = 25
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")

def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS_LEVEL):
        self._log(SUCCESS_LEVEL, message, args, **kwargs)

logging.Logger.success = success
# ================================

from chronilog.core.formatter import build_console_handler, build_file_formatter
from chronilog.core.handlers import get_file_handler
from chronilog.core.config import get_log_level

_loggers = {}

def ChroniLog(
    name: str,
    level: int = None,
    console_formatter: logging.Formatter = None,
    file_formatter: logging.Formatter = None,
    use_cache: bool = True,
    enable_console: bool = False  # 🔹 New: toggle console logging
) -> logging.Logger:
    """
    Initializes and returns a Chronilog logger instance.

    Args:
        name (str): Name of the logger (usually __name__ or module identifier).
        level (int, optional): Override log level (default: config-based).
        console_formatter (logging.Formatter, optional): Override console format.
        file_formatter (logging.Formatter, optional): Override file format.
        use_cache (bool): If True, return cached logger if already initialized.
        enable_console (bool): If True, attach console output. Default is False.

    Returns:
        logging.Logger: Configured logger instance.
    """
    if use_cache and name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)
    logger.setLevel(level or get_log_level())
    logger.propagate = False

    if not use_cache:
        logger.handlers.clear()

    if not logger.handlers:
        # 🟩 File Handler (Always added)
        file_handler = get_file_handler()
        file_handler.setFormatter(file_formatter or build_file_formatter())
        logger.addHandler(file_handler)

        # 🟨 Optional Console Handler
        if enable_console:
            console_handler = build_console_handler()
            console_handler.setFormatter(console_formatter or None)  # Rich handles its own formatting
            logger.addHandler(console_handler)

    if use_cache:
        _loggers[name] = logger

    return logger
