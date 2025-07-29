import asyncio
import logging
import sys
from os import getenv

from dotenv import load_dotenv

import holocal

load_dotenv()
logging.basicConfig(
    level=(getenv("HOLOCAL_LOGLEVEL") or "INFO").upper(),
    format="[{levelname}][{module}][{funcName}] {message}",
    style='{'
)

log = logging.getLogger()

if __name__ == "__main__":
    # argparse いる？ 使わなそう…
    holocal_page = getenv(
        "HOLOCAL_PAGE") or "https://schedule.hololive.tv/simple"
    youtube_key = getenv("HOLOCAL_YOUTUBE_KEY")
    save_dir = getenv("HOLOCAL_DIR") or "public"

    if not holocal_page:
        log.critical("no holocal_page is given")
        sys.exit(1)

    if not youtube_key:
        log.critical("no youtube_key is given")
        sys.exit(1)

    h = holocal.Holocal(holocal_page,
                          youtube_key, save_dir)
    sys.exit(asyncio.run(h.run()))
