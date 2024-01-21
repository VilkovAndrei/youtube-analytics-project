import os
from googleapiclient.discovery import build

api_key: str = os.getenv('YOUTUBE_API_KEY')


class YoutubeService:

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=api_key)
