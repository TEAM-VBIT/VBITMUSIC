import re
import aiohttp
import asyncio
from yt_dlp import YoutubeDL
from config import API_URL, API_KEY

# बोट कॉलिंग इंजन (call.py) के लिए आवश्यक ग्लोबल वेरिएबल
cookie_txt_file = None

class YouTubeAPI:
    def __init__(self):
        self.api_url = API_URL
        self.api_key = API_KEY
        # Termux API डाउन होने की स्थिति में इमरजेंसी लोकल बैकअप कॉन्फ़िगरेशन
        self.opts = {
            "format": "bestaudio/best",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "geo_bypass": True,
            "nocheckcertificate": True,
            "quiet": True,
        }

    async def fetch_stream_url(self, video_id: str):
        """
        यह फंक्शन तुम्हारे टर्मक्स Serveo API गेटवे को हिट करके डायरेक्ट हाई-स्पीड स्ट्रीमिंगリンク फेच करता है।
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
                # लोकल फॉलबैक (अगर टर्मक्स टनल काम न करे)
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

    async def exists(self, link: str, videoid: bool = False):
        """
        /play, /vplay, /cplay कमांड्स के लिए यूआरएल वेरिफिकेशन सिस्टम।
        """
        if videoid:
            return True
        if not link:
            return False
        if "youtu.be" in str(link) or "youtube.com" in str(link):
            return True
        return False

    def extract_id(self, url: str):
        """
        यूट्यूब यूआरएल से 11 डिजिट की यूनिक वीडियो आईडी एक्सट्रैक्ट करने का रेगुलर एक्सप्रेशन।
        """
        regex = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
        match = re.search(regex, url)
        if match:
            return match.group(1)
        return None

    async def url(self, message_or_url):
        """
        टेलीग्राम संदेश टेक्स्ट या इनपुट सर्च क्वेरी को प्रोसेस करके वैलिड यूट्यूब लिंक फॉर्मेट में बदलता है।
        """
        if hasattr(message_or_url, "text"):
            text = message_or_url.text.split(None, 1)
            url_str = text[1].strip() if len(text) > 1 else ""
        else:
            url_str = str(message_or_url).strip()
            
        if not url_str:
            return None
            
        video_id = self.extract_id(url_str)
        if video_id:
            return f"https://youtube.com{video_id}"
            
        # अगर यूआरएल की जगह गाने का नाम भेजा गया है तो उसे सर्च करें
        search_results = await self.search(url_str, limit=1)
        if search_results and isinstance(search_results, list):
            return f"https://youtube.com{search_results[0]['id']}"
        return None

    async def details(self, url: str, forceplay: bool = False):
        """
        प्लेबैक शुरू होने से पहले बोट कोर इसी मेथड से गानों का मेटाडेटा अनपैक करता है।
        """
        video_id = self.extract_id(url)
        if not video_id:
            return None, None, None, None
            
        res = await self.fetch_stream_url(video_id)
        if res.get("status"):
            title = res.get("title")
            duration = res.get("duration")
            thumbnail = f"https://youtube.com{video_id}/hqdefault.jpg"
            return title, duration, thumbnail, video_id
        return None, None, None, None

    async def search(self, query: str, limit: int = 1):
        """
        यूट्यूब सर्च इंजन जो कीवर्ड के आधार पर गानों की लिस्ट निकालता है।
        """
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
        """
        यूट्यूब प्लेलिस्ट डाउनलोड और बल्क स्ट्रीमिंग को सपोर्ट करने के लिए।
        """
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

# बोट कंपोनेंट्स में आसानी से इम्पोर्ट करने के लिए इंस्टेंस इनिशियलाइजेशन
youtube_downloader = YouTubeAPI()
