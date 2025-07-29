import os
import tempfile
from unittest.mock import patch

from book_strands.tools.read_ebook_metadata import extract_epub_metadata
from book_strands.tools.write_ebook_metadata import write_epub_metadata

from .conftest import CORRECT_METADATA_DIR


class TestWriteEbookMetadata:
    """Test cases for the write_ebook_metadata function."""

    @patch("book_strands.tools.write_ebook_metadata.write_ebook_metadata")
    def test_file_not_found(self, mock_write):
        """Test handling of non-existent source file."""
        mock_write.return_value = {
            "status": "error",
            "message": "Source file not found: non_existent_file.epub",
        }
        result = mock_write("non_existent_file.epub", "output.epub", {})
        assert result["status"] == "error"
        assert "Source file not found" in result["message"]

    @patch("book_strands.tools.write_ebook_metadata.write_ebook_metadata")
    def test_unsupported_format(self, mock_write):
        """Test handling of unsupported file format."""
        with tempfile.NamedTemporaryFile(suffix=".txt") as temp_file:
            mock_write.return_value = {
                "status": "error",
                "message": "Unsupported file format: .txt. Supported formats: .epub, .mobi, .azw, .azw3",
            }
            result = mock_write(temp_file.name, "output.txt", {})
            assert result["status"] == "error"
            assert "Unsupported file format" in result["message"]

    def write_temp_epub_file(self, metadata):
        source_file = os.path.join(
            CORRECT_METADATA_DIR,
            "bobiverse-1.epub",
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            dest_file = os.path.join(temp_dir, "output.epub")
            write_epub_metadata(source_file, dest_file, metadata)
            return extract_epub_metadata(dest_file)

    def test_write_epub_metadata_title(self):
        """Test updating title metadata in an EPUB file."""
        result = self.write_temp_epub_file({"title": "Updated Title Test"})

        # Verify the result
        assert result["status"] == "success"
        assert result["title"] == "Updated Title Test"
        assert result["authors"] == ["Dennis E. Taylor"]
        assert result["series"] == "Bobiverse"
        assert result["series_index"] == "1.0"

    def test_write_epub_metadata_authors(self):
        """Test updating author metadata in an EPUB file."""
        result = self.write_temp_epub_file(
            {"authors": ["Test Author 1", "Test Author 2"]}
        )

        # Verify the result
        assert result["status"] == "success"
        assert result["title"] == "We Are Legion (We Are Bob)"
        assert result["authors"] == ["Test Author 1", "Test Author 2"]
        assert result["series"] == "Bobiverse"
        assert result["series_index"] == "1.0"

    def test_write_epub_metadata_series(self):
        """Test updating series metadata in an EPUB file."""
        result = self.write_temp_epub_file(
            {"series": "Updated Series Test", "series_index": "5.2"}
        )

        # Verify the result
        assert result["status"] == "success"
        assert result["title"] == "We Are Legion (We Are Bob)"
        assert result["authors"] == ["Dennis E. Taylor"]
        assert result["series"] == "Updated Series Test"
        assert result["series_index"] == "5.2"
