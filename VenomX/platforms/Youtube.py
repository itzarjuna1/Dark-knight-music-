
# All rights reserved.
#
import asyncio
import os
import random
import re

from async_lru import alru_cache
from youtubesearchpython import VideosSearch
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from yt_dlp import YoutubeDL

import config
from VenomX.utils.database import is_on_off
from VenomX.utils.decorators import asyncify
from VenomX.utils.formatters import seconds_to_min, time_to_seconds

NOTHING = {"cookies_dead": None}


def cookies():
    folder_path = f"{os.getcwd()}/cookies"
    txt_files = [file for file in os.listdir(folder_path) if file.endswith(".txt")]
    if not txt_files:
        raise FileNotFoundError(
            "No Cookies found in cookies directory. Make sure your cookies file is a .txt file."
        )
    cookie_txt_file = random.choice(txt_files)
    return os.path.join(folder_path, cookie_txt_file)


async def shell_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, errorz = await proc.communicate()
    if errorz and "unavailable videos are hidden" not in errorz.decode().lower():
        return errorz.decode()
    return out.decode()


class YouTube:
    def init(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|
