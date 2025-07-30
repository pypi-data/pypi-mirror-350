"""Command-line interface for the data handler."""
import click
from loguru import logger

from .cdc_handler import CDCHandler
from .config_loader import load_config


@click.group()
def cli():
    """Data handler CLI."""
    pass


@cli.command()
@click.option("--config", required=True, help="Path to configuration file")
def sync(config):
    """Run a one-time sync."""
    try:
        config_data = load_config(config)
        handler = CDCHandler(config_data)
        handler.sync()
    except Exception as e:
        logger.error(f"Error during sync: {str(e)}")
        raise click.ClickException(str(e))


@cli.command()
@click.option("--config", required=True, help="Path to configuration file")
def continuous_sync(config):
    """Run continuous sync."""
    try:
        config_data = load_config(config)
        handler = CDCHandler(config_data)
        handler.run_continuous()
    except Exception as e:
        logger.error(f"Error during continuous sync: {str(e)}")
        raise click.ClickException(str(e))


if __name__ == "__main__":
    cli() 