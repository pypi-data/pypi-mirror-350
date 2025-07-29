import os
import sys
import tempfile

from .conftest import CORRECT_METADATA_DIR

# Add the parent directory to path to ensure imports work correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from book_strands.tools.read_ebook_metadata import (
    extract_epub_metadata,
    read_ebook_metadata,
)


class TestReadEbookMetadata:
    """Test cases for the read_ebook_metadata function."""

    def test_file_not_found(self):
        """Test handling of non-existent file."""
        result = read_ebook_metadata("non_existent_file.epub")  # type: ignore
        assert result["status"] == "error"
        assert "File not found" in result["message"]

    def test_unsupported_format(self):
        """Test handling of unsupported file format."""

        with tempfile.NamedTemporaryFile(suffix=".txt") as temp_file:
            result = read_ebook_metadata(temp_file.name)  # type: ignore
            assert result["status"] == "error"
            assert "Unsupported file format" in result["message"]

    def test_extract_epub_metadata_bobiverse(self):
        """Test reading metadata from bobiverse-1.epub."""
        test_file = os.path.join(
            CORRECT_METADATA_DIR,
            "bobiverse-1.epub",
        )
        result = extract_epub_metadata(test_file)

        assert result["status"] == "success"
        assert result["title"] == "We Are Legion (We Are Bob)"
        assert "Dennis E. Taylor" in result["authors"]
        assert result["series"] == "Bobiverse"
        assert result["series_index"] == "1.0"
        assert result["isbn"] is not None

    def test_extract_epub_metadata_gods_of_risk(self):
        """Test reading metadata from gods-of-risk.epub."""
        test_file = os.path.join(
            CORRECT_METADATA_DIR,
            "gods-of-risk.epub",
        )
        result = extract_epub_metadata(test_file)

        assert result["status"] == "success"
        assert result["title"] == "Gods of Risk: An Expanse Novella"

        assert "James S. A. Corey" in result["authors"]
        assert result["series"] == "The Expanse"
        assert result["series_index"] == "2.5"
        assert result["isbn"] is not None
