import sys

from pathlib import Path

from loguru import logger

LOG_DIRE = "logs"
LOG_FILE_FORMAT = "{time:YYYY-MM-DD}.log"
LOG_ROTATION = "100 MB"
try:
    log_path = Path(LOG_DIRE)
    log_path.mkdir(exist_ok=True)
    (log_path / ".gitignore").write_text("*", encoding="utf-8")
except Exception as e:
    print(f"Failed to initialize log directory: {e}", file=sys.stderr)

logger.remove()

log_levels = {
    "DEBUG": "<magenta>",
    "INFO": "<green>",
    "SUCCESS": "<cyan>",
    "WARNING": "<yellow>",
    "ERROR": "<red>",
    "CRITICAL": "<bold><red>",
}

for level_name, color in log_levels.items():
    logger.level(level_name, color=color)

logger.add(
    sys.stderr,
    backtrace=False,
    diagnose=False,
    colorize=True,
    level="DEBUG",
    format="<level>{level: <8}</level> | <cyan>{name}:{function}:{line}</cyan> - <level>{message}</level>",
)
logger.add(
    f"{LOG_DIRE}/{LOG_FILE_FORMAT}",
    rotation=LOG_ROTATION,
    enqueue=True,
    backtrace=False,
    diagnose=False,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
    compression="gz",
)
