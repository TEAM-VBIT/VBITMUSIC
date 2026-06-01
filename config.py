from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        self.API_ID = int(getenv("API_ID", "39665202"))
        self.API_HASH = getenv("API_HASH", "97e021acb4dd34a06986576fc7214ec7")

        self.BOT_TOKEN = getenv("BOT_TOKEN")
        self.MONGO_URL = getenv("MONGO_URL")

        self.LOGGER_ID = int(getenv("LOGGER_ID", "-1002267263891"))
        self.OWNER_ID = int(getenv("OWNER_ID", "5576295421"))

        self.DURATION_LIMIT = int(getenv("DURATION_LIMIT", "10800"))
        self.QUEUE_LIMIT = int(getenv("QUEUE_LIMIT", "20"))
        self.PLAYLIST_LIMIT = int(getenv("PLAYLIST_LIMIT", "20"))

        self.SESSION1 = getenv("SESSION")
        self.SESSION2 = getenv("SESSION2")
        self.SESSION3 = getenv("SESSION3")

        self.SUPPORT_CHANNEL = getenv(
            "SUPPORT_CHANNEL",
            "https://t.me/VAMPIREUPDATES"
        )

        self.SUPPORT_CHAT = getenv(
            "SUPPORT_CHAT",
            "https://t.me/VAMPIREUPDATES"
        )

        self.AUTO_END = getenv(
            "AUTO_END",
            "False"
        ).lower() == "true"

        self.AUTO_LEAVE = getenv(
            "AUTO_LEAVE",
            "False"
        ).lower() == "true"

        self.VIDEO_PLAY = getenv(
            "VIDEO_PLAY",
            "True"
        ).lower() == "true"

        self.COOKIES_URL = [
            url
            for url in getenv("COOKIES_URL", "").split()
            if url
        ]

        # xBit API
        self.YTPROXY_URL = getenv(
            "YTPROXY_URL",
            "https://tgapi.xbitcode.com"
        )

        self.YT_API_KEY = getenv(
            "YT_API_KEY",
            "xbit_26LDtCp-c1wtWGnbrQ68jrkdKrVQpFNS"
        )

        self.YOUTUBE_API_KEY = getenv(
            "YOUTUBE_API_KEY",
            self.YT_API_KEY
        )

        self.DEFAULT_THUMB = getenv(
            "DEFAULT_THUMB",
            "https://te.legra.ph/file/3e40a408286d4eda24191.jpg"
        )

        self.PING_IMG = getenv(
            "PING_IMG",
            "https://i.ibb.co/fzQJvwB9/x.jpg"
        )

        self.START_IMG = getenv(
            "START_IMG",
            "https://i.ibb.co/fzQJvwB9/x.jpg"
        )

    def check(self):
        required = {
            "API_ID": self.API_ID,
            "API_HASH": self.API_HASH,
            "BOT_TOKEN": self.BOT_TOKEN,
            "MONGO_URL": self.MONGO_URL,
            "LOGGER_ID": self.LOGGER_ID,
            "OWNER_ID": self.OWNER_ID,
            "SESSION1": self.SESSION1,
        }

        missing = [
            key for key, value in required.items()
            if value in [None, "", 0]
        ]

        if missing:
            raise SystemExit(
                f"Missing required environment variables: {', '.join(missing)}"
            )


config = Config()

# Backward compatibility
API_ID = config.API_ID
API_HASH = config.API_HASH
BOT_TOKEN = config.BOT_TOKEN
MONGO_URL = config.MONGO_URL
LOGGER_ID = config.LOGGER_ID
OWNER_ID = config.OWNER_ID

YT_API_KEY = config.YT_API_KEY
YTPROXY_URL = config.YTPROXY_URL
YOUTUBE_API_KEY = config.YOUTUBE_API_KEY
