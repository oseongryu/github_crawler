import json
import os

import isodate
# from dotenv import load_dotenv
from googleapiclient.discovery import build

# 채널 ID 배열
CHANNEL_IDS = [
    "UCLkAepWjdylmXSltofFvsYQ",  # BTS
    "UC9GtSLeksfK4yuJ_g1lgQbg",  # AESPA
    "UCOmHUn--16B90oW2L6FRR3A",  # BLACKPINK
    "UCMki_UkHb4qSc0qyEcOHHJw",  # NEWJEANS
    "UCod5V2dpnpJLklGvVOv5FcQ",  # STAYC
    "UC-Fnix71vRP64WXeo0ikd0Q",  # IVE
    "UCDhM2k2Cua-JdobAh5moMFg",  # ITZY
    "UC8whlOg70m2Yr3qSMjUhh0g",  # KEP1ER
]

# load_dotenv()
API_KEY = os.environ.get('YOUTUBE_KEY')
# API_KEY = os.getenv("YOUTUBE_KEY")  # 실제 API 키로 교체


def get_channel_shorts(channel_id, max_count=50):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    channel_response = youtube.channels().list(part="contentDetails", id=channel_id).execute()
    uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    playlist_response = youtube.playlistItems().list(part="snippet", playlistId=uploads_playlist_id, maxResults=50).execute()
    video_ids = [item["snippet"]["resourceId"]["videoId"] for item in playlist_response["items"]]
    videos_response = youtube.videos().list(part="contentDetails,snippet", id=",".join(video_ids)).execute()
    shorts_data = []
    for video in videos_response["items"]:
        duration = isodate.parse_duration(video["contentDetails"]["duration"])
        if duration.total_seconds() <= 60:
            video_id = video["id"]
            shorts_data.append(video_id)
            if len(shorts_data) >= max_count:
                break
    return shorts_data


if __name__ == "__main__":
    save_dir = os.path.join(os.path.dirname(__file__), "locale/en")
    os.makedirs(save_dir, exist_ok=True)
    for idx, channel_id in enumerate(CHANNEL_IDS, 1):
        try:
            shorts_ids = get_channel_shorts(channel_id, max_count=50)
            file_path = os.path.join(save_dir, f"video{idx}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump({"1": shorts_ids}, f, ensure_ascii=False, indent=4)
            print(f"{file_path} 저장 완료 ({len(shorts_ids)}개)")
        except Exception as e:
            print(f"{channel_id} 처리 중 오류 발생: {e}")
