# YouTubeMusic 🔥
A blazing fast YouTube music search module using DuckDuckGo scraping.

## Features

- No YouTube API needed ✅
- Fast + lightweight async search engine ⚡
- Perfect for Telegram bots, CLI tools, and more 🎧

## Install

```bash
pip install YouTubeMusic

```
# How To Install

```bash
# Search By YouTube Search API
from YouTubeMusic.YtSearch import Search

# Search Using Httpx And Re
from YouTubeMusic.Search import Search
```


# Example Usage
```python

from YouTubeMusic.Search import Search
#from YouTubeMusic.YtSearch import Search

async def SearchYt(query: str):
    results = await Search(query, limit=1)

    if not results:
        raise Exception("No results found.")

    search_data = []
    for item in results:
        search_data.append({
            "title": item["title"],
            "artist": item["artist_name"],
            "channel": item["channel_name"],
            "duration": item["duration"],
            "views": item["views"],
            "thumbnail": item["thumbnail"],
            "url": item["url"]
        })

    stream_url = results[0]["url"]
    
    return search_data, stream_url
```
