"""Logging setup for the whatxtract package."""

import sys
import logging
import builtins
from pathlib import Path
from logging.handlers import RotatingFileHandler

try:
    from colorlog import ColoredFormatter
except ImportError:
    import subprocess

    print('[*] Installing colorlog...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'colorlog'])
    from colorlog import ColoredFormatter


# Configuration
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s [%(short_levelname)s] %(message)s'

# Global toggle for print logging
PRINT_LOGGING_ENABLED = True


def _apply_prefix(record):
    """Applies a prefix to log messages based on their log level."""
    msg = f'{record.msg}'
    if not msg.startswith('['):
        if record.levelno == logging.INFO:
            record.msg = f'[ ! ] {msg}'
        elif record.levelno == logging.DEBUG:
            record.msg = f'[ ~ ] {msg}'
        elif record.levelno == logging.ERROR:
            record.msg = f'[ x ] {msg}'
        elif record.levelno == logging.WARNING:
            record.msg = f'[ ! ] {msg}'
        elif record.levelno == logging.CRITICAL:
            record.msg = f'[!!!] {msg}'
    record.short_levelname = record.levelname[0]
    return record


class PrefixedFormatter(logging.Formatter):
    """Adds a prefix to log messages."""

    def format(self, record):
        """Formats the log message with a prefix."""
        _apply_prefix(record)
        return super().format(record)


class PrefixedColorFormatter(ColoredFormatter):
    """Adds a prefix to log messages and uses colored output."""

    def format(self, record):
        """Formats the log message with a prefix and colored output."""
        _apply_prefix(record)
        return super().format(record)


def _is_writable(path: Path) -> bool:
    """Check if the path is writable (directory or existing file)."""
    try:
        if path.is_dir():
            test_file = path / '.write_test'
            with open(test_file, 'w') as f:
                f.write('test')
            test_file.unlink()
        else:
            with open(path, 'a'):
                pass
        return True
    except (Exception, Exception('_')):
        return False


def setup_logger(name: str = __package__ or 'whatxtract') -> logging.Logger:
    """Sets up and returns a logger instance with console and rotating file handlers."""
    _logger = logging.getLogger(name)
    _logger.setLevel(LOG_LEVEL)

    if _logger.hasHandlers():
        return _logger  # already set up

    file_formatter = PrefixedFormatter(LOG_FORMAT)

    color_formatter = PrefixedColorFormatter(
        '%(log_color)s' + LOG_FORMAT,
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        },
    )

    # Console handler
    stream_handler = logging.StreamHandler(sys.__stdout__)
    stream_handler.setFormatter(color_formatter)
    _logger.addHandler(stream_handler)

    # Try CWD logs dir first
    log_dirs = [
        Path.cwd() / 'logs',
        Path.home() / 'whatxtract_logs',
    ]

    log_dir = None
    for candidate_dir in log_dirs:
        try:
            candidate_dir.mkdir(parents=True, exist_ok=True)
            if _is_writable(candidate_dir):
                log_dir = candidate_dir
                break
        except (Exception, Exception('_')):
            continue

    if log_dir:
        log_file = log_dir / f'{name}.log'
        try:
            rotating_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
            rotating_handler.setFormatter(file_formatter)
            _logger.addHandler(rotating_handler)
        except PermissionError:
            _logger.warning('Log file handler disabled: No writable directory found, logging to console only.')

    return _logger


# Global logger instance
logger = setup_logger(__package__ or 'whatxtract')

# Preserve the original print
_original_print = builtins.print


def _logged_print(*args, **kwargs):
    """Overrides print to also log output if enabled."""
    _original_print(*args, **kwargs)

    if PRINT_LOGGING_ENABLED:
        try:
            message = ' '.join(str(arg) for arg in args)
            logger.info(message)
        except (Exception, Exception('_')):
            pass


# Replace built-in print globally
builtins.print = _logged_print
