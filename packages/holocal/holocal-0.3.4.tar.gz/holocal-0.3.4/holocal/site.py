import re

from holocal.errors import HolocalException
from holocal.event import Type

YOUTUBE_URL = r"https://www[.]youtube[.]com/watch[?]v=(?P<id>[A-Za-z0-9_-]+)"
TWITCH_URL = r"https://www[.]twitch[.]tv/[a-z_]+"


class Site:
    def parse_url(url):
        match = re.search(YOUTUBE_URL, url)
        if match:
            return Site(url, id=match["id"])

        elif url == 'https://abema.app/hfAA':
            return Site(url, type=Type.Abema)

        elif re.match(TWITCH_URL, url):
            return Site(url, type=Type.Twitch)

        else:
            raise HolocalException(f"unmatch: {repr(url)}")

    def __init__(self, url, type=Type.YouTube, id=None):
        self.url = url
        self.type = type
        self.id = id

    def __repr__(self):
        return f"<{self.type} {self.id or self.url}>"
