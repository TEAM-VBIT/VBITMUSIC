import re
import aiohttp
import asyncio
from yt_dlp import YoutubeDL
from config import API_URL, API_KEY

class YouTubeAPI:
    def __init__(self):
        self.api_url = API_URL
        self.api_key = API_KEY
        # Fallback options if Termux API fails
        self.opts = {
            "format": "bestaudio/best",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "geo_bypass": True,
            "nocheckcertificate": True,
            "quiet": True,
        }

    async def fetch_stream_url(self, video_id: str):
        """
        यह फंक्शन तुम्हारे टर्मक्स पर चल रहे Serveo API को हिट करेगा 
        और वहाँ से डायरेक्ट सिक्योर हाई-स्पीड स्ट्रीमिंग लिंक निकाल कर लाएगा।
        """
        params = {
            "key": self.api_key,
            "id": video_id
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.api_url, params=params, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("status") == "success":
                            return {
                                "status": True,
                                "title": data.get("title", "Nickbeat Stream Node"),
                                "stream_url": data.get("stream_url"),
                                "duration": data.get("duration", "03:30"),
                                "quality": data.get("quality", "High Fidelity")
                            }
                        else:
                            return {"status": False, "error": data.get("error", "Unknown API Error")}
                    elif response.status == 403:
                        return {"status": False, "error": "API Key Invalid!"}
                    else:
                        return {"status": False, "error": f"Termux Status: {response.status}"}
            except Exception as e:
                # Termux API डाउन होने पर Local Fallback (ताकि बोट बंद न हो)
                try:
                    loop = asyncio.get_running_loop()
                    with YoutubeDL(self.opts) as ydl:
                        info = await loop.run_in_executor(None, lambda: ydl.extract_info(f"https://youtube.com{video_id}", download=False))
                        return {
                            "status": True,
                            "title": info.get("title"),
                            "stream_url": info.get("url"),
                            "duration": info.get("duration"),
                            "quality": "Local Fallback"
                        }
                except Exception as ex:
                    return {"status": False, "error": f"Both API and Local Fallback failed: {str(ex)}"}

    # --- बोट के लिए ज़रूरी अन्य सभी कोर फंक्शन्स ---

    def extract_id(self, url: str):
        regex = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
        match = re.search(regex, url)
        if match:
            return match.group(1)
        return None

    async def search(self, query: str, limit: int = 1):
        loop = asyncio.get_running_loop()
        with YoutubeDL({"quiet": True, "extract_flat": True}) as ydl:
            try:
                info = await loop.run_in_executor(None, lambda: ydl.extract_info(f"ytsearch{limit}:{query}", download=False))
                if "entries" in info and info["entries"]:
                    return info["entries"]
                return []
            except Exception:
                return []

    async def playlist(self, url: str, limit: int = 25):
        loop = asyncio.get_running_loop()
        with YoutubeDL({"quiet": True, "extract_flat": True}) as ydl:
            try:
                info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=False))
                tracks = []
                if "entries" in info:
                    for entry in info["entries"][:limit]:
                        if entry:
                            tracks.append({
                                "title": entry.get("title"),
                                "id": entry.get("id"),
                                "duration": entry.get("duration")
                            })
                return tracks
            except Exception:
                return []

# ऑब्जेक्ट इनिशियलाइजेशन ताकि बोट इसे आसानी से इम्पोर्ट कर सके
youtube_downloader = YouTubeAPI()
