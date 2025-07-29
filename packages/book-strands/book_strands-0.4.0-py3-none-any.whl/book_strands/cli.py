import json
import logging
import os

import click

from .agent import agent
from .constants import SUPPORTED_FORMATS
from .tools.read_ebook_metadata import read_ebook_metadata
from .tools.write_ebook_metadata import write_ebook_metadata

CONTEXT_SETTINGS = {"help_option_names": ["--help", "-h"]}

log = logging.getLogger(__name__)


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Book Strands CLI tool."""
    pass


@cli.command()
@click.argument("path", type=click.Path(exists=True))
def read_book(path):
    """Read ebook metadata from a file or folder.

    PATH is the path to an ebook file (.epub, .mobi, .azw, .azw3)
    """
    result = read_ebook_metadata(path)

    # Format the output nicely
    click.echo(json.dumps(result, indent=2))


@cli.command()
@click.argument("source", type=click.Path(exists=True))
@click.argument("destination", type=click.Path())
@click.option("--title", help="Book title")
@click.option("--authors", help="Comma-separated list of authors")
@click.option("--series", help="Series name")
@click.option("--series-index", help="Position in series")
@click.option("--description", help="Book description in HTML format")  # <-- New option
def write_book(source, destination, title, authors, series, series_index, description):
    """Write metadata to an ebook file.

    SOURCE is the path to the source ebook file
    DESTINATION is the path where the modified file will be saved
    """
    # Prepare the metadata dictionary
    metadata = {}

    # Use provided values or fall back to existing metadata
    if title:
        metadata["title"] = title

    if authors:
        metadata["authors"] = [author.strip() for author in authors.split(",")]

    if series:
        metadata["series"] = series
        if series_index:
            metadata["series_index"] = series_index

    if description:
        metadata["html_description"] = description

    result = write_ebook_metadata(
        source_file_path=source,
        destination_file_path=destination,
        metadata=metadata,  # type: ignore
    )

    if result.get("status") == "success":
        click.echo(result.get("message"))
    elif result.get("status") == "warning":
        click.echo(f"Warning: {result.get('message')}")
    else:
        click.echo(f"Error: {result.get('message', 'Unknown error')}")


@cli.command()
@click.argument("input-path", type=click.Path(exists=True))
@click.argument("output-path", type=click.Path())
@click.option(
    "--output-format",
    default="{{author}}/{{series}}/{{title}}.{{extension}}",
    show_default=True,
    help="Output format for the renamed files",
)
@click.option(
    "--ollama",
    default=False,
    is_flag=True,
    help="Use an Ollama model instead of Bedrock",
)
@click.option(
    "--ollama-model", default="qwen3:8b", show_default=True, help="Ollama model to use"
)
@click.option(
    "--ollama-url",
    default="http://localhost:11434",
    show_default=True,
    help="Ollama server URL",
)
def run(input_path, output_path, output_format, ollama, ollama_model, ollama_url):
    """Run the Book Strands agent."""

    input_files = []

    for root, _, filenames in os.walk(input_path):
        for filename in filenames:
            if filename.endswith(SUPPORTED_FORMATS):
                input_files.append(os.path.join(root, filename))

    if not input_files:
        click.echo("No supported ebook files found.")
        return

    log.info(f"Found {len(input_files)} supported ebook files.")
    log.debug(f"Input files: {input_files}")

    agent(
        input_files=input_files,
        output_path=output_path,
        output_format=output_format,
        ollama_config={"use_ollama": ollama, "model": ollama_model, "url": ollama_url},
    )
