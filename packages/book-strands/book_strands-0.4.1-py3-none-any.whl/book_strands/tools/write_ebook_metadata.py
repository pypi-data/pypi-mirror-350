import logging
import os
import shutil
import subprocess

from strands import tool

from book_strands.constants import SUPPORTED_FORMATS
from book_strands.utils import ebook_meta_binary, file_extension

log = logging.getLogger(__name__)


@tool
def write_ebook_metadata(
    source_file_path: str, destination_file_path: str, metadata: dict
) -> dict:
    """
    Write metadata to ebook files using Calibre's ebook-meta CLI tool.

    Args:
        source_file_path (str): Path to the source ebook file
        destination_file_path (str): Path to save the modified file
        metadata (dict): A dictionary containing metadata to write. All fields are optional. Supported keys:
        {
            "title": str,
            "authors": list of str,
            "series": str,
            "series_index": str,
            "html_description": str,
        }

    Returns:
        A dictionary containing status of the operation in the format:
        {
            "status": "success" or "error",
            "message": "Description of the operation result"
        }
    """
    log.info(f"Starting metadata write for file: {source_file_path}")
    log.debug(f"Destination file: {destination_file_path}")
    log.debug(f"Metadata to write: {metadata}")

    source_file_path = os.path.expanduser(source_file_path)
    destination_file_path = os.path.expanduser(destination_file_path)

    # Check if source file exists
    if not os.path.exists(source_file_path):
        log.error(f"Source file not found: {source_file_path}")
        return {
            "status": "error",
            "message": f"Source file not found: {source_file_path}",
        }

    # Ensure the destination directory exists
    dest_dir = os.path.dirname(os.path.abspath(destination_file_path))
    log.debug(f"Creating destination directory if needed: {dest_dir}")
    os.makedirs(dest_dir, exist_ok=True)

    ext = file_extension(source_file_path)
    if ext in SUPPORTED_FORMATS:
        log.info(f"Found supported ebook format file: {ext}")
        return write_metadata(source_file_path, destination_file_path, metadata)
    else:
        log.error(f"Unsupported file format: {ext}")
        return {
            "status": "error",
            "message": f"Unsupported file format: {ext}. Supported formats: {', '.join(SUPPORTED_FORMATS)}",
        }


def build_ebook_meta_command(file_path, metadata):
    """Build the ebook-meta command list for subprocess.run, using the correct path for macOS."""

    cmd = [ebook_meta_binary(), file_path]
    if "title" in metadata and metadata["title"]:
        cmd.append(f"--title={metadata['title']}")
    if "authors" in metadata and metadata["authors"]:
        cmd.append(f"--authors={' & '.join(metadata['authors'])}")
    if "series" in metadata and metadata["series"]:
        cmd.append(f"--series={metadata['series']}")
    if "series_index" in metadata and metadata["series_index"]:
        cmd.append(f"--index={str(metadata['series_index'])}")
    if "html_description" in metadata and metadata["html_description"]:
        cmd.append(f"--comments={metadata['html_description']}")
    return cmd


def write_metadata(source_file_path, destination_file_path, metadata):
    """Write metadata to EPUB files using Calibre's ebook-meta CLI tool"""
    log.info("Writing metadata to file using ebook-meta")
    try:
        log.debug("Copying source file to destination")
        shutil.copy(source_file_path, destination_file_path)

        cmd = build_ebook_meta_command(destination_file_path, metadata)

        log.info(f"Running ebook-meta command: {' '.join(cmd)}")
        try:
            subprocess.check_output(cmd)
        except subprocess.CalledProcessError as e:
            log.error(f"ebook-meta command failed: {e}")
            return {
                "status": "error",
                "message": f"ebook-meta command failed: {e.stderr.decode('utf-8')} {e.stdout.decode('utf-8')}",
            }

        return {
            "status": "success",
            "message": f"Metadata written successfully to {destination_file_path}",
        }

    except Exception as e:
        log.error(f"Error writing EPUB metadata: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": f"Error writing EPUB metadata: {str(e)}",
        }
