"""Constants for tests."""

from importlib import metadata

version =  "1"

HEADERS = {
    "User-Agent": f"python-zinvolt/{version}",
    "Authorization": "Bearer token"
}

URL = "https://eva-backoffice.onmoonly.app/api/public/v2/"
