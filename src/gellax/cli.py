"""Command-line interface for Gellax."""
import logging
from typing import List
import click

from .core import process_items

logger = logging.getLogger(__name__)


@click.command()
@click.argument("items", nargs=-1)
@click.option("--verbose", is_flag=True, default=False, help="Enable verbose logging")
def main(items: List[str], verbose: bool):
    """Run processing on ITEMS and print results.

    Example: `gellax hello world`
    """
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)
    logger.info("Running Gellax on %d items", len(items))
    res = process_items(list(items))
    for r in res:
        click.echo(r)


if __name__ == "__main__":
    main()
