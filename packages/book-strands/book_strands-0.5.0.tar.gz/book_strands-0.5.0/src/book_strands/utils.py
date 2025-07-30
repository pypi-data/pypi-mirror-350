import os
import sys
from configparser import ConfigParser
from functools import lru_cache

from book_strands.constants import CONFIG_FILE_PATH


def file_extension(file_path):
    """Get the file extension of a file"""
    _, ext = os.path.splitext(file_path)
    return ext.lower()


@lru_cache(maxsize=1)
def load_book_strands_config() -> ConfigParser:
    """Loads and caches the config from ~/.book-strands.conf as a ConfigParser object."""
    config_path = os.path.expanduser(CONFIG_FILE_PATH)
    config = ConfigParser()
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at {config_path}")
    config.read(config_path)
    return config


def ebook_meta_binary():
    """Get the path to the ebook-meta binary"""
    if sys.platform == "darwin":
        return "/Applications/calibre.app/Contents/MacOS/ebook-meta"
    else:
        return "ebook-meta"
