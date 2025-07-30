# Apigle Python Client

A Python client for the Apigle API, providing YouTube-like data endpoints.

## Installation

Install dependencies:

```bash
pip install apigle
```

## Quick Start

```python
from apigle.client import ApigleClient

API_KEY = "YOUR_API_KEY"
client = ApigleClient(API_KEY)
```

## Functions & Usage Examples

### 1. Video Search (v1)
```python
result = client.search_v1(q="lofi music")
print(result)
```
Search for videos by keyword.

---

### 2. Get Download URL & Metadata (v2)
```python
## Available options for resolution: 360,720,1080,2160
info = client.download(video="QW8-UVmMm_Q", type="mp4", resolution=360)
print(info["url"])
```
Returns a download URL and metadata for the video. Does not download the file.

---

### 3. Download Video File
```python
## Available options for resolution: 360,720,1080,2160
success = client.download_file(video="QW8-UVmMm_Q", output_path="video.mp4", type="mp4", resolution=360)
print("Downloaded:", success)
```
Downloads the video file to the specified path. Returns True if successful.

---

### 4. Advanced Video Search (v2)
```python
result = client.search_v2(q="ban", part="snippet", regionCode="US", maxResults=100, order="relevance")
print(result)
```
Search with more parameters for advanced filtering.

---

### 5. Video Comments
```python
result = client.video_comments(videoId="kffacxfA7G4", part="snippet", maxResults=100)
print(result)
```
List comments for a video.

---

### 6. Video Details
```python
result = client.video_details(id="XGGXlj6grzQ", part="contentDetails,snippet,statistics")
print(result)
```
Get detailed information about a video.

---

### 7. Channel Details
```python
result = client.channel_details(id="UCfM3zsQsOnfWNUppiycmBuw", part="snippet,statistics")
print(result)
```
Get detailed information about a channel.

---

### 8. Channel Videos
```python
result = client.channel_videos(channelId="UCvgfXK4nTYKudb0rFR6noLA", part="snippet,id", order="date", maxResults=50)
print(result)
```
List videos from a channel.

---

### 9. Playlist Details
```python
result = client.playlist_details(id="PLqpXi64f6ul2Nzd5hHdHS4XuWa7ix8Rm-", part="snippet")
print(result)
```
Get details of a playlist.

---

### 10. Playlist Videos
```python
result = client.playlist_videos(playlistId="RDMM", part="snippet", maxResults=50)
print(result)
```
List videos in a playlist.

---

### 11. Trending Videos
```python
result = client.trending(part="snippet", videoCategoryId=1, regionCode="US", maxResults=50)
print(result)
```
List trending videos for a category and region.

---

### 12. Video Categories
```python
result = client.video_categories(part="snippet")
print(result)
```
List all video categories.

---

### 13. Supported Regions (i18nRegions)
```python
result = client.i18n_regions()
print(result)
```
List all supported regions/countries.

---

## Testing

You can write your own tests or use the provided examples in the `examples/` directory to see how each endpoint works. For real-world usage, integrate the client into your own Python scripts or applications.

## License
MIT
