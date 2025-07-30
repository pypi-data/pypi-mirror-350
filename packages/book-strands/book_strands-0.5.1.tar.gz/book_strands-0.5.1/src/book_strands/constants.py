SUPPORTED_FORMATS = (
    "epub",
    "mobi",
    "azw",
    "azw3",
)  # In priority order for downloads

CONFIG_FILE_PATH = "~/.config/book-strands.conf"
ZLIB_BASE_URL = "https://z-library.sk"
ZLIB_SEARCH_URL = f"{ZLIB_BASE_URL}/s/"
ZLIB_LOGIN_URL = f"{ZLIB_BASE_URL}/rpc.php"
ZLIB_LOGOUT_URL = f"{ZLIB_BASE_URL}/papi/user/logout"
ZLIB_PROFILE_URL = f"{ZLIB_BASE_URL}/profile"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
}
