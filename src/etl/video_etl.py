from googleapiclient.discovery import build
import pandas as pd
from dotenv import load_dotenv
import os

# Load .env file dari parent directory (src)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def extract_video_data(video_ids):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    metadata = []

    for vid in video_ids:
        response = youtube.videos().list(part="snippet,statistics", id=vid).execute()
        for item in response['items']:
            snippet = item['snippet']
            stats = item['statistics']
            metadata.append({
                "video_id": item["id"],
                "channel_id": snippet["channelId"],
                "channel_title": snippet["channelTitle"],
                "title": snippet["title"],
                "published_at": snippet["publishedAt"],
                "view_count": stats.get("viewCount"),
                "like_count": stats.get("likeCount"),
                "comment_count": stats.get("commentCount"),
                "favorite_count": stats.get("favoriteCount"),
            })
    return pd.DataFrame(metadata)

def load_video_data_to_csv(video_data, filename="data/videos_metadata.csv"):
    dir_name = os.path.dirname(filename)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    video_data.to_csv(filename, index=False)

def etl_video_data(video_ids):
    video_data = extract_video_data(video_ids)
    load_video_data_to_csv(video_data)