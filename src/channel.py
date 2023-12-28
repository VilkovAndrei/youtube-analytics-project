import json
import os

from googleapiclient.discovery import build

api_key: str = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    @property
    def channel_id(self) -> str:
        return self.__channel_id

    def __init__(self, str_channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = str_channel_id

        channel_dict = Channel.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        channel_items = channel_dict['items'][0]

        self.title = channel_items['snippet']['title']
        self.description = channel_items['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{str_channel_id}"
        self.subscribers_count = int(channel_items['statistics']['subscriberCount'])
        self.video_count = int(channel_items['statistics']['videoCount'])
        self.views_count = int(channel_items['statistics']['viewCount'])

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, filename):
        channel_info = {"title": self.title,
                        "channel_id": self.channel_id,
                        "description": self.description,
                        "url": self.url,
                        "subscribers_count": self.subscribers_count,
                        "video_count": self.video_count,
                        "views_count": self.views_count}
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(channel_info, file, indent=4, ensure_ascii=False)
