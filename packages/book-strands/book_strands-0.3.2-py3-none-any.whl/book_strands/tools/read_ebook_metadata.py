import logging
import os
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

import ebooklib
from ebooklib import epub
from strands import tool

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


@tool
def read_ebook_metadata(file_path: str) -> dict:
    """
    Extract metadata from EPUB or MOBI ebook files.

    Args:
        file_path: Path to the EPUB or MOBI file

    Returns:
        A dictionary containing metadata such as title, authors, series, series_number, and ISBN
    """
    file_path = os.path.expanduser(file_path)

    # Check if file exists
    if not os.path.exists(file_path):
        return {"status": "error", "message": f"File not found: {file_path}"}

    # Check file extension
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".epub":
        log.info("Found epub format file")
        return extract_epub_metadata(file_path)
    elif ext in [".mobi", ".azw", ".azw3"]:
        log.info("Found mobi format file")
        return extract_mobi_metadata(file_path)
    else:
        return {
            "status": "error",
            "message": f"Unsupported file format: {ext}. Supported formats: .epub, .mobi, .azw, .azw3",
        }


def extract_epub_metadata(file_path):
    """Extract metadata from EPUB files using ebooklib"""
    try:
        book = epub.read_epub(file_path)
        metadata = {}

        # Extract title
        metadata["title"] = get_epub_metadata_item(book, "title")

        # Extract authors
        metadata["authors"] = get_epub_metadata_items(book, "creator")

        # Extract ISBN
        metadata["isbn"] = get_epub_metadata_item(book, "identifier")

        # Try to extract series information
        metadata["series"] = None
        metadata["series_index"] = None

        try:
            series_metadata = book.get_metadata(
                "http://calibre.kovidgoyal.net/2009/metadata", "series"
            )[0][1]
            if series_metadata["name"] == "calibre:series":
                metadata["series"] = series_metadata["content"]
        except Exception:
            pass

        try:
            series_index_metadata = book.get_metadata(
                "http://calibre.kovidgoyal.net/2009/metadata", "series_index"
            )[0][1]
            if series_index_metadata["name"] == "calibre:series_index":
                metadata["series_index"] = series_index_metadata["content"]
        except Exception:
            pass

        # Try calibre metadata format
        try:
            ns = {
                "opf": "http://www.idpf.org/2007/opf",
                "dc": "http://purl.org/dc/elements/1.1/",
            }
            for item in book.get_items():
                if (
                    isinstance(item, ebooklib.epub.EpubItem)
                    and item.get_type() == ebooklib.ITEM_DOCUMENT
                ):
                    content = item.get_content().decode("utf-8")
                    if "calibre:series" in content:
                        root = ET.fromstring(content)
                        series_elem = root.find(".//meta[@name='calibre:series']", ns)
                        series_index_elem = root.find(
                            ".//meta[@name='calibre:series_index']", ns
                        )
                        if series_elem is not None:
                            metadata["series"] = series_elem.get("content")
                        if series_index_elem is not None:
                            metadata["series_index"] = series_index_elem.get("content")
        except Exception:
            pass

        metadata["status"] = "success"
        return metadata
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error extracting EPUB metadata: {str(e)}",
        }


def extract_mobi_metadata(file_path):
    """Extract metadata from MOBI files using kindleunpack if available or mobi library"""
    try:
        # First try using the command-line kindleunpack tool if available
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Check if KindleUnpack is available
                result = subprocess.run(
                    ["kindleunpack", "-h"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=1,
                )

                # If available, use kindleunpack
                result = subprocess.run(
                    ["kindleunpack", file_path, temp_dir],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=10,
                )

                # Process extracted files
                metadata = {}
                opf_file = None

                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith(".opf"):
                            opf_file = os.path.join(root, file)
                            break
                    if opf_file:
                        break

                if opf_file:
                    tree = ET.parse(opf_file)
                    root = tree.getroot()

                    namespaces = {
                        "dc": "http://purl.org/dc/elements/1.1/",
                        "opf": "http://www.idpf.org/2007/opf",
                    }

                    # Get title
                    title_elem = root.find(".//dc:title", namespaces)
                    if title_elem is not None and title_elem.text:
                        metadata["title"] = title_elem.text

                    # Get authors
                    authors = []
                    for author_elem in root.findall(".//dc:creator", namespaces):
                        if author_elem.text:
                            authors.append(author_elem.text)
                    metadata["authors"] = authors if authors else None

                    # Get ISBN
                    for identifier in root.findall(".//dc:identifier", namespaces):
                        id_text = identifier.text if identifier.text else ""
                        if "isbn" in id_text.lower() or (
                            len(id_text) in [10, 13] and id_text.isdigit()
                        ):
                            metadata["isbn"] = id_text
                            break
                    else:
                        metadata["isbn"] = None

                    # Try to get series information
                    metadata["series"] = None
                    metadata["series_number"] = None

                    # Check for Calibre series metadata
                    for meta in root.findall(".//meta", namespaces):
                        name = meta.get("name", "")
                        content = meta.get("content", "")

                        if name == "calibre:series" and content:
                            metadata["series"] = content
                        elif name == "calibre:series_index" and content:
                            metadata["series_number"] = content

                    # We no longer look for series info in the title
                    # Only rely on calibre metadata for series information

                    metadata["status"] = "success"
                    return metadata
                else:
                    # Fallback to basic metadata extraction
                    return extract_basic_mobi_metadata(file_path)

            except (subprocess.SubprocessError, FileNotFoundError):
                # Fallback to basic metadata extraction
                return extract_basic_mobi_metadata(file_path)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error extracting MOBI metadata: {str(e)}",
        }


def extract_basic_mobi_metadata(file_path):
    """Basic MOBI metadata extraction fallback using direct file inspection"""
    try:
        # Basic extraction by examining MOBI file directly
        metadata = {
            "status": "warning",
            "message": "Limited metadata extracted - full extraction requires kindleunpack tool",
        }

        with open(file_path, "rb") as f:
            content = f.read()

            # Try to extract title
            title_match = re.search(rb"<dc:title>(.*?)</dc:title>", content)
            if title_match:
                metadata["title"] = title_match.group(1).decode(
                    "utf-8", errors="ignore"
                )
            else:
                metadata["title"] = Path(file_path).stem

            # Try to extract authors
            authors = []
            author_matches = re.findall(
                rb"<dc:creator[^>]*>(.*?)</dc:creator>", content
            )
            for author in author_matches:
                authors.append(author.decode("utf-8", errors="ignore"))

            metadata["authors"] = authors if authors else None

            # Try to extract ISBN
            isbn_match = re.search(
                rb"<dc:identifier[^>]*isbn[^>]*>(.*?)</dc:identifier>",
                content,
                re.IGNORECASE,
            )
            metadata["isbn"] = (
                isbn_match.group(1).decode("utf-8", errors="ignore")
                if isbn_match
                else None
            )

            # Don't attempt to infer series from title
            metadata["series"] = None
            metadata["series_number"] = None

        return metadata

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error in basic MOBI metadata extraction: {str(e)}",
        }


def get_epub_metadata_item(book, name):
    """Helper function to get a single metadata item from an EPUB book"""
    items = get_epub_metadata_items(book, name)
    return items[0] if items else None


def get_epub_metadata_items(book, name):
    """Helper function to get all metadata items with a given name from an EPUB book"""
    items = []
    try:
        for item in book.get_metadata("DC", name):
            items.append(item[0])
    except Exception:
        pass
    return items
