import os
import sys


def file_extension(file_path):
    """Get the file extension of a file"""
    _, ext = os.path.splitext(file_path)
    return ext.lower()


def ebook_meta_binary():
    """Get the path to the ebook-meta binary"""
    if sys.platform == "darwin":
        return "/Applications/calibre.app/Contents/MacOS/ebook-meta"
    else:
        return "ebook-meta"
