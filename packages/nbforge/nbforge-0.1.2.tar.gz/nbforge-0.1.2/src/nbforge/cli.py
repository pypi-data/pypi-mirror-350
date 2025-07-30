import click
from nbforge.converter import convert_notebook
from nbforge.logger import setup_logger

logger = setup_logger(__name__)


@click.group()
def cli():
    """
    Command-line interface group for NBForge commands.

    Args:
        None

    Returns:
        None
    """
    pass


@cli.command()
@click.argument("notebook_path")
@click.argument("output_directory")
def convert(notebook_path, output_directory):
    """
    Converts a Jupyter notebook to a structured Python project.

    Args:
        notebook_path (str): Path to the Jupyter notebook file.
        output_directory (str): Directory where the output files will be written.

    Returns:
        None
    """
    convert_notebook(notebook_path, output_directory)


def main():
    """
    Entry point for the NBForge CLI.

    Args:
        None

    Returns:
        None
    """
    cli()
