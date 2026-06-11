import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# --- ⚠️ VAMPIRE MUSIC BOT CORE CONFIG ---
API_ID = int(getenv("API_ID", "29869035"))
API_HASH = getenv("API_HASH", "e7543eeb90a3209df9ee6b26aa84f994")
BOT_TOKEN = getenv("BOT_TOKEN", "8962093065:AAEve-UeHcfipFSGq4Q3IqXbyL0X9FdA7nA")
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://TEAM-VAMPIRE-OP:VAMPIRE800@team-vampire-op.npkrxta.mongodb.net/?appName=TEAM-VAMPIRE-OP")

# --- 🌐 NICKBEAT TERMUX API GATEWAY SETTINGS ---
API_URL = getenv("API_URL", "https://1785987ec9867259-122-183-45-61.serveousercontent.com")
API_KEY = getenv("API_KEY", "NICK_OWNER_7260HA") 

# Fallback variables mapped to your Termux API link to fix the API endpoint errors
YTPROXY_URL = getenv("YTPROXY_URL", API_URL)
YT_API_KEY = getenv("YT_API_KEY", API_KEY)

## Other variables
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", "180"))
LOGGER_ID = int(getenv("LOGGER_ID", "-1002654645615"))
OWNER_ID = int(getenv("OWNER_ID", "8725368443"))

## Fill these variables if you're deploying on heroku.
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/TEAM-VBIT/VBITMUSIC",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv("GIT_TOKEN", None)  # Fill this variable if your upstream repository is private

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/llNICK_UPDATESll")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/llDEAR_NICKll")

# Set this to True if you want the assistant to automatically leave chats after an interval
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", True))
ASSISTANT_LEAVE_TIME = int(getenv("ASSISTANT_LEAVE_TIME", 5400))

# Get this credentials from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "1c21247d714244ddbb09925dac565aed")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "709e1a2969664491b58200860623ef19")

# Maximum limit for fetching playlist's track from youtube, spotify, apple links.
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))

# Telegram audio and video file size limit (in bytes)
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 204857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 2073741824))

PRIVATE_BOT_MODE_MEM = int(getenv("PRIVATE_BOT_MODE_MEM", 1))

CACHE_DURATION = int(getenv("CACHE_DURATION", "86400"))  #60*60*24
CACHE_SLEEP = int(getenv("CACHE_SLEEP", "3600"))   #60*60

# Get your pyrogram v2 session from @StringFatherBot on Telegram
STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}
file_cache: dict[str, float] = {}

START_IMG_URL = ["https://i.ibb.co/fzQJvwB9/x.jpg",
                 "https://i.ibb.co/fzQJvwB9/x.jpg",
                 "https://i.ibb.co/fzQJvwB9/x.jpg"]
    
PING_IMG_URL = getenv("PING_IMG_URL", "https://i.ibb.co/RG1B0F8L/x.jpg")
PLAYLIST_IMG_URL = "https://graph.org/file/c95a687e777b55be1c792.jpg"
STATS_IMG_URL = "https://telegra.ph/file/edd388a42dd2c499fd868.jpg"
TELEGRAM_AUDIO_URL = "https://telegra.ph/file/492a3bb2e880d19750b79.jpg"
TELEGRAM_VIDEO_URL = "https://telegra.ph/file/492a3bb2e880d19750b79.jpg"
STREAM_IMG_URL = "https://graph.org/file/ff2af8d4d10afa1baf49e.jpg"
SOUNCLOUD_IMG_URL = "https://graph.org/file/c95a687e777b55be1c792.jpg"
YOUTUBE_IMG_URL = "https://graph.org/file/e8730fdece86a1166f608.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://graph.org/file/0bb6f36796d496b4254ff.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://graph.org/file/0bb6f36796d496b4254ff.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://graph.org/file/0bb6f36796d496b4254ff.jpg"

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:360"))

if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )
