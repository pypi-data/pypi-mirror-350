from .tools.read_ebook_metadata import read_ebook_metadata
from strands import Agent
from strands_tools import http_request
import logging

# Enables Strands debug log level
logging.getLogger("strands").setLevel(logging.DEBUG)

# Sets the logging format and streams logs to stderr
logging.basicConfig(
    format="%(asctime)s %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()],
)
