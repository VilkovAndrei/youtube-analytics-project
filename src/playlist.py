import json
import datetime
from isodate import parse_duration
from src.youtube_service import YoutubeService


class PlayList(YoutubeService):
    """Класс для ютуб-плей-листа"""

    @property
    def pl_id(self) -> str:
        return self.__pl_id

    def __init__(self, str_pl_id: str):
        """Экземпляр инициализируется id плей-листа. Дальше все данные будут подтягиваться по API."""
        self.__pl_id = str_pl_id

        pl_dict = PlayList.get_service().playlists().list(id=self.pl_id, part='snippet').execute()
        self.title: str = pl_dict['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.pl_id}"

    def __str__(self):
        return f"{self.title}"

    def print_info(self) -> None:
        """Выводит в консоль информацию о видео."""
        pl_dict = PlayList.get_service().playlists().list(id=self.pl_id, part='snippet').execute()
        print(json.dumps(pl_dict, indent=2, ensure_ascii=False))

    def to_json(self, filename):
        pl_info = {"title": self.title,
                   "pl_id": self.pl_id,
                   "url": self.url}
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(pl_info, file, indent=4, ensure_ascii=False)

    @property
    def total_duration(self) -> datetime.timedelta:
        playlist_videos = PlayList.get_service().playlistItems().list(playlistId=self.pl_id,
                                                                      part='contentDetails',
                                                                      maxResults=50,).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = PlayList.get_service().videos().list(part='contentDetails,statistics',
                                                              id=','.join(video_ids)).execute()
        total_time = datetime.timedelta()
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = parse_duration(iso_8601_duration)
            total_time += duration
        return total_time

    def show_best_video(self):
        playlist_videos = PlayList.get_service().playlistItems().list(playlistId=self.pl_id,
                                                                      part='contentDetails',
                                                                      maxResults=50,).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        max_like_count = 0
        current_video_id = ''
        for video_id in video_ids:
            video_response = PlayList.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                                  id=video_id).execute()
            like_count: int = int(video_response['items'][0]['statistics']['likeCount'])
            if like_count > max_like_count:
                max_like_count = like_count
                current_video_id = video_id
        return f"https://youtu.be/{current_video_id}"
