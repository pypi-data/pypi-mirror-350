import httpx
import re
import json
from .Utils import parse_dur, format_views

def Search(query: str, limit: int = 1):
    search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = httpx.get(search_url, headers=headers, timeout=10)
    match = re.search(r"var ytInitialData = ({.*?});</script>", response.text)
    if not match:
        return []

    data = json.loads(match.group(1))
    results = []

    try:
        videos = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]\
            ["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]

        for item in videos:
            if "videoRenderer" in item:
                v = item["videoRenderer"]
                title = v["title"]["runs"][0]["text"]
                video_id = v["videoId"]
                url = f"https://www.youtube.com/watch?v={video_id}"
                duration = v.get("lengthText", {}).get("simpleText", "LIVE")
                views = v.get("viewCountText", {}).get("simpleText", "0")
                channel_name = v["ownerText"]["runs"][0]["text"]
                thumbnail = v["thumbnail"]["thumbnails"][-1]["url"]

                results.append({
                    "type": "video",
                    "title": title,
                    "artist_name": channel_name,
                    "channel_name": channel_name,
                    "views": format_views(views),
                    "duration": duration,
                    "thumbnail": thumbnail,
                    "url": url,
                })

            elif "playlistRenderer" in item:
                p = item["playlistRenderer"]
                title = p["title"]["runs"][0]["text"]
                playlist_id = p["playlistId"]
                url = f"https://www.youtube.com/playlist?list={playlist_id}"
                video_count = p.get("videoCount", "0")
                thumbnail = p["thumbnails"][0]["thumbnails"][-1]["url"]
                channel_name = p["shortBylineText"]["runs"][0]["text"]

                results.append({
                    "type": "playlist",
                    "title": title,
                    "channel_name": channel_name,
                    "video_count": video_count,
                    "thumbnail": thumbnail,
                    "url": url,
                })

            if len(results) >= limit:
                break

    except Exception as e:
        print("Error:", e)

    return results
