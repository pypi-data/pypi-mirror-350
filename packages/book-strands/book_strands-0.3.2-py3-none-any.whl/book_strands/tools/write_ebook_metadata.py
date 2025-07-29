import logging
import os
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET

from ebooklib import epub
from strands import tool

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


@tool
def write_ebook_metadata(
    source_file_path: str, destination_file_path: str, metadata: dict
) -> dict:
    """
    Write metadata to EPUB or MOBI ebook files.

    Args:
        source_file_path (str): Path to the source EPUB or MOBI file
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

    # Check file extension
    ext = os.path.splitext(source_file_path)[1].lower()
    log.debug(f"File extension: {ext}")

    # Ensure the destination directory exists
    dest_dir = os.path.dirname(os.path.abspath(destination_file_path))
    log.debug(f"Creating destination directory if needed: {dest_dir}")
    os.makedirs(dest_dir, exist_ok=True)

    if ext == ".epub":
        log.info("Found epub format file")
        return write_epub_metadata(source_file_path, destination_file_path, metadata)
    elif ext in [".mobi", ".azw", ".azw3"]:
        log.info("Found mobi format file")
        return write_mobi_metadata(source_file_path, destination_file_path, metadata)
    else:
        log.error(f"Unsupported file format: {ext}")
        return {
            "status": "error",
            "message": f"Unsupported file format: {ext}. Supported formats: .epub, .mobi, .azw, .azw3",
        }


def write_epub_metadata(source_file_path, destination_file_path, metadata):
    """Write metadata to EPUB files using ebooklib"""
    log.info(f"Writing metadata to EPUB file: {source_file_path}")
    try:
        log.debug("Loading EPUB book")
        book = epub.read_epub(source_file_path)

        if "title" in metadata and metadata["title"]:
            log.info(f"Updating title to: {metadata['title']}")
            book.metadata["http://purl.org/dc/elements/1.1/"]["title"] = [
                (metadata["title"], {})
            ]

        if "authors" in metadata and metadata["authors"]:
            log.info(f"Updating authors to: {metadata['authors']}")
            # Remove existing creators (authors)
            book.metadata["http://purl.org/dc/elements/1.1/"]["creator"] = []

            for author in metadata["authors"]:
                log.debug(f"Adding author: {author}")
                author_block = (
                    author,
                    {
                        "{http://www.idpf.org/2007/opf}role": "aut",
                        "{http://www.idpf.org/2007/opf}file-as": author,
                    },
                )
                book.metadata["http://purl.org/dc/elements/1.1/"]["creator"].append(
                    author_block
                )

        if "series" in metadata and metadata["series"]:
            log.info(f"Updating series to: {metadata['series']}")
            book.metadata["http://calibre.kovidgoyal.net/2009/metadata"]["series"] = [
                (
                    None,
                    {
                        "name": "calibre:series",
                        "content": metadata["series"],
                    },
                )
            ]
            book.metadata["http://www.idpf.org/2007/opf"][None] = [
                (
                    "series",
                    {"refines": "#id-1", "property": "collection-type"},
                ),
                (
                    metadata["series"],
                    {"property": "belongs-to-collection", "id": "id-1"},
                ),
            ]

            if "series_index" in metadata and metadata["series_index"]:
                log.info(f"Updating series index to: {metadata['series_index']}")
                book.metadata["http://calibre.kovidgoyal.net/2009/metadata"][
                    "series_index"
                ] = [
                    (
                        None,
                        {
                            "name": "calibre:series_index",
                            "content": metadata["series_index"],
                        },
                    )
                ]
                book.metadata["http://www.idpf.org/2007/opf"][None].append(
                    (
                        metadata["series_index"],
                        {"refines": "#id-1", "property": "group-position"},
                    )
                )

        if "html_description" in metadata and metadata["html_description"]:
            log.info(f"Updating description to: {metadata['html_description']}")
            book.metadata["http://purl.org/dc/elements/1.1/"]["description"] = [
                (metadata["html_description"], None)
            ]

        log.info(f"Writing updated EPUB to: {destination_file_path}")
        epub.write_epub(destination_file_path, book)

        log.info("EPUB metadata update completed successfully")
        return {
            "status": "success",
            "message": f"Successfully updated EPUB metadata and saved to {destination_file_path}",
        }
    except Exception as e:
        log.error(f"Error writing EPUB metadata: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": f"Error writing EPUB metadata: {str(e)}",
        }


def write_mobi_metadata(source_file_path, destination_file_path, metadata):
    """Write metadata to MOBI files using kindleunpack if available"""
    log.info(f"Writing metadata to MOBI file: {source_file_path}")
    try:
        # First, we need to copy the source file to the destination
        # since we don't have a direct way to modify MOBI files in-place
        log.debug(f"Copying source file to destination: {destination_file_path}")
        shutil.copy2(source_file_path, destination_file_path)

        # Check if kindleunpack and kindlegen are available for proper MOBI handling
        try:
            # Check if KindleUnpack is available
            log.debug("Checking if KindleUnpack is available")
            subprocess.run(
                ["kindleunpack", "-h"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=1,
            )

            # Check if kindlegen is available
            log.debug("Checking if kindlegen is available")
            subprocess.run(
                ["kindlegen", "-h"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=1,
            )

            log.info(
                "KindleUnpack and kindlegen tools found, proceeding with MOBI metadata update"
            )
            # If both are available, we can use them to modify the MOBI
            with tempfile.TemporaryDirectory() as temp_dir:
                log.debug(f"Created temporary directory: {temp_dir}")

                # Extract the MOBI with kindleunpack
                log.info("Extracting MOBI with kindleunpack")
                result = subprocess.run(
                    ["kindleunpack", source_file_path, temp_dir],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=10,
                )
                log.debug(f"Kindleunpack output: {result.stdout}")
                if result.stderr:
                    log.warning(f"Kindleunpack stderr: {result.stderr}")

                # Find the OPF file
                log.debug("Searching for OPF file in extracted MOBI")
                opf_file = None
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith(".opf"):
                            opf_file = os.path.join(root, file)
                            log.debug(f"Found OPF file: {opf_file}")
                            break
                    if opf_file:
                        break

                if not opf_file:
                    log.error("Could not find OPF file in extracted MOBI")
                    return {
                        "status": "error",
                        "message": "Could not find OPF file in extracted MOBI",
                    }

                # Modify the OPF file with updated metadata
                log.info("Modifying OPF file with updated metadata")
                tree = ET.parse(opf_file)
                root = tree.getroot()

                namespaces = {
                    "dc": "http://purl.org/dc/elements/1.1/",
                    "opf": "http://www.idpf.org/2007/opf",
                }

                # Update title if provided
                if "title" in metadata and metadata["title"]:
                    log.info(f"Updating title to: {metadata['title']}")
                    title_elem = root.find(".//dc:title", namespaces)
                    if title_elem is not None:
                        title_elem.text = metadata["title"]
                        log.debug("Updated existing title element")
                    else:
                        # Create title element if it doesn't exist
                        log.debug("No title element found, creating new one")
                        metadata_elem = root.find(".//opf:metadata", namespaces) or root
                        ET.SubElement(
                            metadata_elem, "{http://purl.org/dc/elements/1.1/}title"
                        ).text = metadata["title"]

                # Update authors if provided
                if "authors" in metadata and metadata["authors"]:
                    log.info(f"Updating authors to: {metadata['authors']}")
                    # Remove existing authors
                    author_count = 0
                    for author_elem in root.findall(".//dc:creator", namespaces):
                        parent = root.find(".//opf:metadata", namespaces) or root
                        parent.remove(author_elem)
                        author_count += 1
                    log.debug(f"Removed {author_count} existing author elements")

                    # Add new authors
                    metadata_elem = root.find(".//opf:metadata", namespaces) or root
                    for author in metadata["authors"]:
                        log.debug(f"Adding author: {author}")
                        ET.SubElement(
                            metadata_elem, "{http://purl.org/dc/elements/1.1/}creator"
                        ).text = author

                # Update series info if provided
                if "series" in metadata and metadata["series"]:
                    log.info(f"Updating series to: {metadata['series']}")
                    # Look for existing calibre series metadata
                    series_found = False
                    for meta in root.findall(".//meta", namespaces):
                        name = meta.get("name", "")
                        if name == "calibre:series":
                            log.debug(
                                f"Found existing series metadata, updating to: {metadata['series']}"
                            )
                            meta.set("content", metadata["series"])
                            series_found = True

                    if not series_found:
                        log.debug("No series metadata found, adding new element")
                        # Add calibre series metadata
                        metadata_elem = root.find(".//opf:metadata", namespaces) or root
                        series_elem = ET.SubElement(metadata_elem, "meta")
                        series_elem.set("name", "calibre:series")
                        series_elem.set("content", metadata["series"])

                    # Handle series index
                    if "series_index" in metadata and metadata["series_index"]:
                        log.info(
                            f"Updating series index to: {metadata['series_index']}"
                        )
                        series_index_found = False
                        for meta in root.findall(".//meta", namespaces):
                            name = meta.get("name", "")
                            if name == "calibre:series_index":
                                log.debug(
                                    f"Found existing series index metadata, updating to: {metadata['series_index']}"
                                )
                                meta.set("content", metadata["series_index"])
                                series_index_found = True

                        if not series_index_found:
                            log.debug(
                                "No series index metadata found, adding new element"
                            )
                            metadata_elem = (
                                root.find(".//opf:metadata", namespaces) or root
                            )
                            series_index_elem = ET.SubElement(metadata_elem, "meta")
                            series_index_elem.set("name", "calibre:series_index")
                            series_index_elem.set("content", metadata["series_index"])

                # Write the modified OPF file
                log.info(f"Writing modified OPF file: {opf_file}")
                tree.write(opf_file, encoding="utf-8", xml_declaration=True)

                # Use kindlegen to rebuild the MOBI
                temp_epub = os.path.join(temp_dir, "temp.epub")
                log.info("Creating temporary EPUB file for conversion")
                # This command is hypothetical and might need adjustment
                rebuild_cmd = f"cd {temp_dir} && zip -r {temp_epub} * && kindlegen {temp_epub} -o temp.mobi"
                log.debug(f"Running rebuild command: {rebuild_cmd}")
                subprocess.run(rebuild_cmd, shell=True, check=True)

                # Copy the rebuilt MOBI to the destination
                rebuilt_mobi = os.path.join(temp_dir, "temp.mobi")
                if os.path.exists(rebuilt_mobi):
                    log.info(
                        f"Copying rebuilt MOBI to destination: {destination_file_path}"
                    )
                    shutil.copy2(rebuilt_mobi, destination_file_path)
                    log.info("MOBI metadata update completed successfully")
                    return {
                        "status": "success",
                        "message": f"Successfully updated MOBI metadata and saved to {destination_file_path}",
                    }
                else:
                    log.error("Failed to rebuild MOBI file - output file not found")
                    return {
                        "status": "error",
                        "message": "Failed to rebuild MOBI file after metadata update",
                    }

        except (subprocess.SubprocessError, FileNotFoundError) as tool_error:
            log.warning(f"KindleUnpack or kindlegen tools not available: {tool_error}")
            # If kindleunpack or kindlegen aren't available, return a limited success
            return {
                "status": "warning",
                "message": f"Limited metadata update capability: file was copied to {destination_file_path} but metadata changes require kindleunpack and kindlegen tools",
            }
    except Exception as e:
        log.error(f"Error writing MOBI metadata: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": f"Error writing MOBI metadata: {str(e)}",
        }
