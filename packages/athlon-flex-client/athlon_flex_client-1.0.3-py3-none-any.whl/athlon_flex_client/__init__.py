"""Top-level package for Athlon Flex Client."""

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_format = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)

from athlon_flex_client.client import AthlonFlexClient  # noqa: E402

__all__ = ["logger", "client", "vehicles_clusters", "AthlonFlexClient"]
