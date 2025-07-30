import requests
import os
from .exceptions import MissingAPIKeyError
from .endpoints import BASE_URL, ENDPOINTS

class ApigleClient:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def set_api_key(self, api_key: str):
        self.api_key = api_key

    def _check_key(self):
        if not self.api_key:
            raise MissingAPIKeyError()

    def _get_headers(self):
        self._check_key()
        return {"x-api-key": self.api_key}

    def _get(self, endpoint: str, params=None):
        url = BASE_URL + endpoint
        headers = self._get_headers()
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 403:
            raise MissingAPIKeyError("API key is missing or invalid (HTTP 403)!")

        response.raise_for_status()
        return response.json()

    # /v1/search
    def search_v1(self, q: str, pageToken: str = None):
        params = {"q": q}
        if pageToken:
            params["pageToken"] = pageToken
        return self._get(ENDPOINTS["search_v1"], params)

    # /v2/download
    def download(self, video: str, type: str = "mp4", resolution: int = None):
        params = {"video": video, "type": type}
        if resolution:
            params["resolution"] = resolution
        return self._get(ENDPOINTS["download"], params)
    
    # download and save file using the url from download endpoint response
    def download_file(self, video: str, output_path: str, type: str = "mp4", resolution: int = None) -> bool:
        """
        Download a file using the download endpoint, then fetch the file from the returned url and save it to output_path.
        Returns True if successful, False otherwise.
        """
        try:
            # 1. Get the download info (url) from the API
            response = self.download(video, type=type, resolution=resolution)
            file_url = response.get("url")
            if not file_url:
                return False
            # 2. Download the file from the url
            r = requests.get(file_url, stream=True)
            r.raise_for_status()
            with open(output_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return True
        except Exception as e:
            print(f"Download error: {e}")
            return False

    # /v2/search
    def search_v2(self, q: str, part: str = "snippet", regionCode: str = "US", maxResults: int = 100, order: str = "relevance", pageToken: str = None):
        params = {"q": q, "part": part}
        if regionCode:
            params["regionCode"] = regionCode
        if maxResults:
            params["maxResults"] = maxResults
        if order:
            params["order"] = order
        if pageToken:
            params["pageToken"] = pageToken
        return self._get(ENDPOINTS["search_v2"], params)

    # /v2/videoComments
    def video_comments(self, videoId: str, part: str = "snippet", maxResults: int = 100):
        params = {"videoId": videoId, "part": part, "maxResults": maxResults}
        return self._get(ENDPOINTS["video_comments"], params)

    # /v2/videoDetails
    def video_details(self, id: str, part: str = "contentDetails,snippet,statistics"):
        params = {"id": id, "part": part}
        return self._get(ENDPOINTS["video_details"], params)

    # /v2/channelDetails
    def channel_details(self, id: str, part: str = "snippet,statistics"):
        params = {"id": id, "part": part}
        return self._get(ENDPOINTS["channel_details"], params)

    # /v2/channelVideos
    def channel_videos(self, channelId: str, part: str = "snippet,id", order: str = "date", maxResults: int = 50, pageToken: str = None):
        params = {"channelId": channelId, "part": part, "order": order, "maxResults": maxResults}
        if pageToken:
            params["pageToken"] = pageToken
        return self._get(ENDPOINTS["channel_videos"], params)

    # /v2/playlistDetails
    def playlist_details(self, id: str, part: str = "snippet"):
        params = {"id": id, "part": part}
        return self._get(ENDPOINTS["playlist_details"], params)

    # /v2/playlistVideos
    def playlist_videos(self, playlistId: str, part: str = "snippet", maxResults: int = 50, pageToken: str = None):
        params = {"playlistId": playlistId, "part": part}
        if pageToken:
            params["pageToken"] = pageToken
        return self._get(ENDPOINTS["playlist_videos"], params)

    # /v2/trending
    def trending(self, part: str = "snippet", videoCategoryId: int = 1, regionCode: str = "US", maxResults: int = 50, pageToken: str = None):
        params = {"part": part, "videoCategoryId": videoCategoryId, "regionCode": regionCode, "maxResults": maxResults}
        if pageToken:
            params["pageToken"] = pageToken
        return self._get(ENDPOINTS["trending"], params)

    # /v2/videoCategories
    def video_categories(self, part: str = "snippet"):
        params = {"part": part}
        return self._get(ENDPOINTS["video_categories"], params)

    # /v2/i18nRegions
    def i18n_regions(self):
        return self._get(ENDPOINTS["i18n_regions"])

