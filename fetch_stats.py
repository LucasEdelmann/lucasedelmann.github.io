import os
import json
import re
from datetime import datetime
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import URLError

API_KEY = os.environ.get("YT_API_KEY")

def extract_video_id(url):
    """Extract YouTube video ID from various URL formats."""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'youtu\.be\/([0-9A-Za-z_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def fetch_video_data(video_ids):
    """Fetch video statistics from YouTube Data API v3."""
    results = []
    # API allows max 50 IDs per request
    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i:i+50]
        params = urlencode({
            "part": "snippet,statistics",
            "id": ",".join(chunk),
            "key": API_KEY
        })
        url = f"https://www.googleapis.com/youtube/v3/videos?{params}"
        try:
            with urlopen(url) as response:
                data = json.loads(response.read())
                for item in data.get("items", []):
                    stats = item.get("statistics", {})
                    snippet = item.get("snippet", {})
                    results.append({
                        "id": item["id"],
                        "title": snippet.get("title", "Unbekannter Titel"),
                        "channel": snippet.get("channelTitle", ""),
                        "published": snippet.get("publishedAt", "")[:10],
                        "views": int(stats.get("viewCount", 0)),
                        "likes": int(stats.get("likeCount", 0)),
                    })
        except URLError as e:
            print(f"API-Fehler: {e}")
    return results

def main():
    # Read video URLs from videos.txt
    with open("videos.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    video_ids = []
    for line in lines:
        vid_id = extract_video_id(line)
        if vid_id:
            video_ids.append(vid_id)
        else:
            print(f"Warnung: Konnte keine Video-ID aus '{line}' extrahieren")

    print(f"{len(video_ids)} Videos gefunden, rufe API ab...")
    videos = fetch_video_data(video_ids)

    total_views = sum(v["views"] for v in videos)
    total_likes = sum(v["likes"] for v in videos)

    output = {
        "last_updated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_views": total_views,
        "total_likes": total_likes,
        "video_count": len(videos),
        "videos": sorted(videos, key=lambda x: x["views"], reverse=True)
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ data.json aktualisiert – {len(videos)} Videos, {total_views:,} Gesamtaufrufe")

if __name__ == "__main__":
    main()
