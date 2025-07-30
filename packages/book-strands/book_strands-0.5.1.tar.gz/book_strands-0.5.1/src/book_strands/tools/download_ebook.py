import logging
import os
import re
from enum import Enum
from os import makedirs
from os.path import dirname
from pathlib import Path
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
from requests import Session
from requests.adapters import HTTPAdapter, Retry
from strands import tool

from book_strands.constants import (
    HEADERS,
    SUPPORTED_FORMATS,
    ZLIB_BASE_URL,
    ZLIB_LOGIN_URL,
    ZLIB_PROFILE_URL,
    ZLIB_SEARCH_URL,
)
from book_strands.utils import load_book_strands_config

WAIT_TIME = 1  # seconds to wait between book downloads and retries

log = logging.getLogger(__name__)


class FileFormat(Enum):
    EPUB = "epub"
    PDF = "pdf"
    MOBI = "mobi"
    AZW3 = "azw3"
    FB2 = "fb2"
    DJVU = "djvu"
    TXT = "txt"
    RTF = "rtf"
    DOC = "doc"
    DOCX = "docx"
    UNDEFINED = "undefined"


class Book(BaseModel):
    title: str
    author: str
    language: str = "English"
    page_url: str = ""
    file_format: FileFormat = FileFormat.UNDEFINED
    download_url: str = ""

    def __repr__(self):
        return f"Book(title={self.title!r}, author={self.author!r})"

    def generate_filename(self):
        """Generate a sanitized filename for the book."""
        filename = f"{self.author} - {self.title}.".title() + self.file_format.value
        return re.sub(r'[<>:"/\\|?*\x00-\x1F]', "_", filename).strip()

    def get_download_url(self, session: Session):
        """Fetch the download URL for the book. The same session must be used for downloading as urls are per-user."""
        if self.download_url:
            log.info(
                f"Download URL already set for book {self.title!r} by {self.author!r}"
            )
            return self.download_url

        if not self.page_url:
            self.get_book_page_url()

        log.info(f"Fetching download link for book: {self.title!r} by {self.author!r}")

        try:
            response = session.get(
                self.page_url, headers={"User-Agent": HEADERS["User-Agent"]}, timeout=10
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            download_tag = soup.find("a", class_="addDownloadedBook")

            if download_tag:
                log.info(f"Found download link: {ZLIB_BASE_URL}{download_tag['href']}")  # type: ignore
                self.download_url = f"{ZLIB_BASE_URL}{download_tag['href']}"  # type: ignore
                return self.download_url

            log.error("No download link found on the book page!")
            raise Exception(
                f"No download link found on the book page for {self.title!r} by {self.author!r}!"
            )

        except Exception as e:
            log.error(
                f"Error fetching download link for {self.title!r} by {self.author!r}: {e}"
            )
            raise e

    def get_book_page_url(self):
        """Search for a book on Z-Library and return a link to the first result."""

        if self.page_url:
            log.info(f"URL already set for book {self.title!r} by {self.author!r}")
        log.info(f"Fetching URL for book: {self.title!r} by {self.author!r}")

        params = {
            "content_type": "book",
            "q": f"{self.title} {self.author}",
        }
        search_url = ZLIB_SEARCH_URL + "?" + urlencode(params)

        log.info(f"Searching for book: {self.title!r} by {self.author!r}")

        try:
            response = requests.get(
                search_url, headers={"User-Agent": HEADERS["User-Agent"]}, timeout=10
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            for ext in SUPPORTED_FORMATS:
                log.debug(f"Searching for books with extension: {ext}")
                book_cards = soup.find_all("z-bookcard", {"extension": ext})
                log.debug(f"Found {len(book_cards)} books with extension {ext}")
                matching_books = [
                    b
                    for b in book_cards
                    if b.get("language").lower() == self.language.lower()  # type: ignore
                ]

                if matching_books:
                    log.info(f"Found matching books with extension {ext}")
                    href = str(matching_books[0].get("href"))  # type: ignore
                    if href:
                        log.info(f"First matching book page URL: {href}")
                        self.page_url = ZLIB_BASE_URL + href
                        self.file_format = FileFormat(ext)
                        return
                log.info(f"No matching books found with extension {ext}.")

        except Exception as e:
            log.error(
                f"Error searching for book {self.title!r} by {self.author!r}: {e}"
            )
            raise e


class DownloadLimitReached(Exception):
    """Raised when the Z-Library download limit has been reached for an account."""

    pass


class ZLibSession(BaseModel):
    email: str
    password: str
    downloads_used: int = 0
    downloads_max: int = 10  # Default max downloads
    session: Session
    logged_in: bool = False

    def __init__(self, **data):
        if "session" not in data or data["session"] is None:
            session = requests.Session()
            retries = Retry(
                total=5,
                backoff_factor=WAIT_TIME,  # wait 1s, 2s, 4s, etc. between retries
                status_forcelist=[500, 502, 503, 504],
                allowed_methods=["GET", "POST"],
            )
            adapter = HTTPAdapter(max_retries=retries)
            session.mount("http://", adapter)
            session.mount("https://", adapter)
            data["session"] = session
        super().__init__(**data)

    class Config:
        arbitrary_types_allowed = True

    def login(self):
        """Logs into Z-Library and returns success status."""
        if self.logged_in:
            log.info(f"Already logged in as {self.email}")
            return True

        self.session.get(ZLIB_LOGIN_URL, headers=HEADERS)

        login_data = {
            "isModal": "true",
            "email": self.email,
            "password": self.password,
            "site_mode": "books",
            "action": "login",
            "redirectUrl": "",
            "gg_json_mode": "1",
        }

        response = self.session.post(
            ZLIB_LOGIN_URL, data=login_data, headers=HEADERS, timeout=10
        )
        if not response:
            log.warning(f"Login failed for {self.email}: No response from server.")
            return False  # Give up after retries

        log.info(f"Login Attempt for: {self.email}")
        log.debug(f"Response Status Code: {response.status_code}")
        log.debug(f"Cookies After Login: {self.session.cookies.get_dict()}")

        success = '"validationError":true' not in response.text
        if success:
            log.info(f"Login successful for {self.email}")
            self._get_download_limits()
            self.logged_in = True

        return success

    def _get_download_limits(self):
        """Fetches the download limits from the user's profile page."""
        html = self.session.get(ZLIB_PROFILE_URL).text
        soup = BeautifulSoup(html, "html.parser")
        titles = soup.find_all("div", class_="caret-scroll__title")

        for title in titles:
            text = title.text.strip()
            log.debug(f"Raw download limit text: '{text}'")
            if "/" in text:
                try:
                    self.downloads_used, self.max_downloads = map(int, text.split("/"))
                    log.info(
                        f"Parsed limits - Used: {self.downloads_used}, Max: {self.max_downloads}"
                    )
                    return
                except ValueError:
                    log.error(f"Failed to parse download limits from text: '{text}'")

        log.error("Could not find download limits. Using default values.")

    def download_book(self, book: Book, destination_folder: str):
        """Downloads the book to the specified file path."""
        if self.downloads_used >= self.downloads_max:
            log.warning(
                f"Download limit reached for {self.email}. Used: {self.downloads_used}, Max: {self.downloads_max}"
            )
            raise DownloadLimitReached(
                f"Download limit reached for {self.email}. Used: {self.downloads_used}, Max: {self.downloads_max}"
            )

        if not book.download_url:
            book.get_download_url(session=self.session)

        destination_file_path = os.path.join(
            destination_folder, book.generate_filename()
        )
        makedirs(dirname(destination_file_path), exist_ok=True)
        Path(destination_file_path).unlink(missing_ok=True)

        log.debug(
            f"Downloading book: {book.title!r} by {book.author!r} using {self.email!r} from {book.download_url!r} to {destination_file_path}"
        )

        try:
            response = self.session.get(
                book.download_url, stream=True, headers=HEADERS, timeout=10
            )
            response.raise_for_status()

            with open(destination_file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            self.downloads_used += 1
            log.info(f"Downloaded book to {destination_file_path}")

        except requests.RequestException as e:
            log.error(
                f"Error downloading book {book.title!r} by {book.author!r}: {e}",
                exc_info=True,
            )
            raise e


class NoLoginsConfigured(Exception):
    """Raised when no zlib-logins are found in the config file."""

    pass


def get_logins():
    """Returns a list of (email, password) tuples from the 'zlib-logins' key in the config."""
    config = load_book_strands_config()

    if "zlib-logins" in config:
        logins = config["zlib-logins"]
    else:
        log.error("'zlib-logins' key not found in config file.")
        raise NoLoginsConfigured("No 'zlib-logins' section found in config file.")

    result = []
    for email, password in logins.items():
        password = password.strip('"')
        result.append((email, password))

    if not result:
        log.error("'zlib-logins' key not found in config file.")
        raise NoLoginsConfigured(
            "No logins found in the 'zlib-logins' section of the config file."
        )
    return result


@tool
def download_ebook(books: list[Book], destination_folder: str) -> bool:
    return _download_ebook(books, destination_folder)


def _download_ebook(books: list[Book], destination_folder: str) -> bool:
    sessions = [
        ZLibSession(email=email, password=password) for email, password in get_logins()
    ]
    session_index = 0

    log.info(f"Starting download process for {len(books)} books.")
    log.debug(f"Books: {[str(book) for book in books]}")

    success = True
    for book in books:
        try:
            while session_index < len(sessions):
                session = sessions[session_index]
                session_index += 1
                if not session.login():
                    log.info(
                        f"Failed to log in with {session.email}. Trying next account."
                    )
                    continue

                try:
                    session.download_book(book, destination_folder)
                except DownloadLimitReached:
                    log.info("Switching accounts due to download limit reached.")
                    session_index += 1
                    continue
        except requests.RequestException as e:
            log.error(
                f"Network error while downloading {book.title!r} by {book.author!r}: {e}"
            )
            success = False
    return success
