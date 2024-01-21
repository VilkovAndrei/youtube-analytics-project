import json

from src.youtube_service import YoutubeService


class Channel(YoutubeService):
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

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return self.subscribers_count + other.subscribers_count

    def __sub__(self, other):
        return self.subscribers_count - other.subscribers_count

    def __gt__(self, other):
        """ Возвращает True или False """
        return self.subscribers_count > other.subscribers_count

    def __ge__(self, other):
        """ Возвращает True или False """
        return self.subscribers_count >= other.subscribers_count

    def __eq__(self, other):
        """ Возвращает True или False """
        return self.subscribers_count == other.subscribers_count

    def __ne__(self, other):
        """ Возвращает True или False """
        return self.subscribers_count != other.subscribers_count

    def __lt__(self, other):
        """ Возвращает True или False """
        return self.subscribers_count < other.subscribers_count

    def __le__(self, other):
        """ Возвращает True или False """
        return self.subscribers_count <= other.subscribers_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = Channel.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

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
