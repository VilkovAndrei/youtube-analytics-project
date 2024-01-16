import os
import json

from googleapiclient.discovery import build

api_key: str = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    """Класс для ютуб-видео"""

    @property
    def video_id(self) -> str:
        return self.__video_id

    def __init__(self, str_video_id: str):
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self.__video_id = str_video_id

        video_dict = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                           id=self.video_id).execute()
        self.video_title: str = video_dict['items'][0]['snippet']['title']
        self.view_count: int = int(video_dict['items'][0]['statistics']['viewCount'])
        self.like_count: int = int(video_dict['items'][0]['statistics']['likeCount'])
        self.video_url = f"https://www.youtube.com/watch?v={self.video_id}"

    def __str__(self):
        return f"{self.video_title}"

    def print_info(self) -> None:
        """Выводит в консоль информацию о видео."""
        video_dict = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                           id=self.video_id).execute()
        print(json.dumps(video_dict, indent=2, ensure_ascii=False))

    def to_json(self, filename):
        video_info = {"video_title": self.video_title,
                      "video_id": self.video_id,
                      "video_url": self.video_url,
                      "view_count": self.view_count,
                      "like_count": self.like_count}
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(video_info, file, indent=4, ensure_ascii=False)


class PLVideo(Video):
    """Класс для ютуб-видео + плей-лист"""

    def __init__(self, str_video_id: str, str_playlist_id: str):
        super().__init__(str_video_id)
        self.playlist_id = str_playlist_id

    def to_json(self, filename):
        video_info = {"video_title": self.video_title,
                      "video_id": self.video_id,
                      "video_url": self.video_url,
                      "view_count": self.view_count,
                      "like_count": self.like_count,
                      "playlist_id": self.playlist_id}
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(video_info, file, indent=4, ensure_ascii=False)
