import re
import aiohttp
import asyncio
from yt_dlp import YoutubeDL
from config import API_URL, API_KEY

# बोट के कोर कॉलिंग इंजन के लिए आवश्यक वेरिएबल
cookie_txt_file = None

class YouTubeAPI:
    def __init__(self):
        self.api_url = API_URL
        self.api_key = API_KEY
        # Termux API फेल होने पर बैकअप ऑप्शन
        self.opts = {
            "format": "bestaudio/best",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "geo_bypass": True,
            "nocheckcertificate": True,
            "quiet": True,
        }

    async def fetch_stream_url(self, video_id: str):
        """
        यह फंक्शन टर्मक्स Serveo API को हिट करके डायरेक्ट स्ट्रीमिंग लिंक लाएगा।
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
                    else:
                        return {"status": False, "error": f"Termux Status: {response.status}"}
            except Exception:
                # लोकल फॉलबैक (अगर टर्मक्स बंद हो)
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
                    return {"status": False, "error": str(ex)}

    def extract_id(self, url: str):
        regex = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
        match = re.search(regex, url)
        if match:
            return match.group(1)
        return None

    async def url(self, message_or_url):
        """
        /play, /vplay, /cplay आदि के यूआरएल चेकर के लिए आवश्यक फंक्शन
        """
        if hasattr(message_or_url, "text"):
            text = message_or_url.text.split(None, 1)
            url_str = text[1] if len(text) > 1 else ""
        else:
            url_str = str(message_or_url)
            
        video_id = self.extract_id(url_str)
        if video_id:
            return f"https://youtube.com{video_id}"
            
        # अगर सिर्फ नाम लिखा है तो सर्च करो
        search_results = await self.search(url_str, limit=1)
        if search_results:
            return f"https://youtube.com{search_results[0]['id']}"
        return None

    async def details(self, url: str, forceplay: bool = False):
        """
        बोट का कोर इंजन गाना प्ले करने से पहले डिटेल्स (Title, Duration, Link) 
        इसी फंक्शन से निकालता है।
        """
        video_id = self.extract_id(url)
        if not video_id:
            return None, None
            
        res = await self.fetch_stream_url(video_id)
        if res.get("status"):
            title = res.get("title")
            duration = res.get("duration")
            # बोट को सीधा स्ट्रीम लिंक देने के लिए हम इसे यहीं इंजेक्ट कर देते हैं
            # AnonXMusic का प्लेबैक डेकोरेटर 'details' से टाइटल और ड्यूरेशन उठाता है
            return title, duration
        return None, None

    async def search(self, query: str, limit: int = 1):
        loop = asyncio.get_running_loop()
        with YoutubeDL({"quiet": True, "extract_flat": True}) as ydl:
            try:
                info = await loop.run_in_executor(None, lambda: ydl.extract_info(f"ytsearch{limit}:{query}", download=False))
                if "entries" in info and info["entries"]:
                    return [{
                        "title": entry.get("title"),
                        "id": entry.get("id"),
                        "duration": entry.get("duration")
                    } for entry in info["entries"] if entry]
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
