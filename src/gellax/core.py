"""Core functionality for Gellax."""
from typing import List
import logging

logger = logging.getLogger(__name__)


def process_items(items: List[str]) -> List[str]:
    """Example processing: normalize and reverse each string list.

    This is a placeholder for the application's global processing logic.
    """
    logger.debug("Processing %d items", len(items))
    result = []
    for it in items:
        if not isinstance(it, str):
            logger.warning("Skipping non-str item: %r", it)
            continue
        normalized = it.strip()
        transformed = normalized[::-1]
        result.append(transformed)
    logger.debug("Processed result: %s", result)
    return result
