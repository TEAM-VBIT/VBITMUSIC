import re
import aiohttp
import asyncio
from yt_dlp import YoutubeDL
from config import API_URL, API_KEY

cookie_txt_file = None


class YouTubeAPI:
    def __init__(self):
        self.api_url = API_URL
        self.api_key = API_KEY

        self.opts = {
            "format": "bestaudio[ext=m4a]/bestaudio/best",
            "geo_bypass": True,
            "nocheckcertificate": True,
            "quiet": True,
            "noplaylist": True,
            "extract_flat": False,
            "cookiefile": cookie_txt_file,
        }

    async def fetch_stream_url(self, video_id: str):
        params = {
            "key": self.api_key,
            "id": video_id,
        }

        if self.api_url and self.api_key:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        self.api_url,
                        params=params,
                        timeout=15,
                    ) as response:

                        if response.status == 200:
                            data = await response.json()

                            if data.get("status") == "success":
                                return {
                                    "status": True,
                                    "title": data.get("title"),
                                    "stream_url": data.get("stream_url"),
                                    "duration": data.get("duration"),
                                    "quality": data.get("quality", "API Stream"),
                                }

            except Exception as e:
                print(f"API ERROR: {e}")

        try:
            loop = asyncio.get_running_loop()

            with YoutubeDL(self.opts) as ydl:
                info = await loop.run_in_executor(
                    None,
                    lambda: ydl.extract_info(
                        f"https://www.youtube.com/watch?v={video_id}",
                        download=False,
                    ),
                )

            return {
                "status": True,
                "title": info.get("title"),
                "stream_url": info.get("url"),
                "duration": info.get("duration"),
                "quality": "Local Fallback",
            }

        except Exception as ex:
            print(f"YTDLP ERROR: {ex}")
            return {
                "status": False,
                "error": str(ex),
            }

    async def exists(self, link: str, videoid: bool = False):
        if videoid:
            return True

        if not link:
            return False

        return (
            "youtube.com" in str(link)
            or "youtu.be" in str(link)
        )

    def extract_id(self, url: str):
        regex = (
            r"(?:youtube\.com\/(?:[^\/]+\/.+\/|"
            r"(?:v|e(?:mbed)?)\/|.*[?&]v=)|"
            r"youtu\.be\/)([^\"&?\/\s]{11})"
        )

        match = re.search(regex, url)

        if match:
            return match.group(1)

        return None

    async def url(self, message_or_url):
        if hasattr(message_or_url, "text"):
            parts = message_or_url.text.split(None, 1)
            query = parts[1].strip() if len(parts) > 1 else ""
        else:
            query = str(message_or_url).strip()

        if not query:
            return None

        video_id = self.extract_id(query)

        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"

        results = await self.search(query, limit=1)

        if results:
            return (
                f"https://www.youtube.com/watch?"
                f"v={results[0]['id']}"
            )

        return None

    async def details(self, url: str, forceplay: bool = False):
        video_id = self.extract_id(url)

        if not video_id:
            return None, None, None, None

        data = await self.fetch_stream_url(video_id)

        if not data.get("status"):
            return None, None, None, None

        title = data.get("title")
        duration = data.get("duration")

        thumbnail = (
            f"https://i.ytimg.com/vi/"
            f"{video_id}/hqdefault.jpg"
        )

        return (
            title,
            duration,
            thumbnail,
            video_id,
        )

    async def search(self, query: str, limit: int = 1):
        try:
            loop = asyncio.get_running_loop()

            with YoutubeDL(
                {
                    "quiet": True,
                    "extract_flat": True,
                    "nocheckcertificate": True,
                }
            ) as ydl:

                info = await loop.run_in_executor(
                    None,
                    lambda: ydl.extract_info(
                        f"ytsearch{limit}:{query}",
                        download=False,
                    ),
                )

            if not info or "entries" not in info:
                return []

            results = []

            for entry in info["entries"]:
                if not entry:
                    continue

                results.append(
                    {
                        "title": entry.get("title"),
                        "id": entry.get("id"),
                        "duration": entry.get("duration"),
                    }
                )

            return results

        except Exception as e:
            print(f"SEARCH ERROR: {e}")
            return []

    async def playlist(self, url: str, limit: int = 25):
        try:
            loop = asyncio.get_running_loop()

            with YoutubeDL(
                {
                    "quiet": True,
                    "extract_flat": True,
                    "nocheckcertificate": True,
                }
            ) as ydl:

                info = await loop.run_in_executor(
                    None,
                    lambda: ydl.extract_info(
                        url,
                        download=False,
                    ),
                )

            tracks = []

            for entry in info.get("entries", [])[:limit]:
                if not entry:
                    continue

                tracks.append(
                    {
                        "title": entry.get("title"),
                        "id": entry.get("id"),
                        "duration": entry.get("duration"),
                    }
                )

            return tracks

        except Exception as e:
            print(f"PLAYLIST ERROR: {e}")
            return []


youtube_downloader = YouTubeAPI()
