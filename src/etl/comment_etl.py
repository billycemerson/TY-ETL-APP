from dotenv import load_dotenv
from googleapiclient.discovery import build
import pandas as pd
import os

# Load .env file from parent directory (src)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def extract_comments(video_id):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    comments = []
    page_token = None

    while True:
        request_kwargs = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": 100,
            "textFormat": "plainText"
        }
        if page_token:
            request_kwargs["pageToken"] = page_token

        response = youtube.commentThreads().list(**request_kwargs).execute()

        for cm in response.get('items', []):
            snip = cm['snippet']['topLevelComment']['snippet']
            comments.append({
                'id_video': video_id,
                'id_komentar': cm['snippet']['topLevelComment']['id'],
                'text_original': snip['textOriginal'],
                'author_name': snip['authorDisplayName'],
                'id_author': snip['authorChannelId']['value'],
                'like_count': snip['likeCount'],
                'published_at': snip['publishedAt']
            })

        page_token = response.get('nextPageToken')
        if not page_token:
            break
    return comments

def load_comments_to_csv(video_id):
    comments = extract_comments(video_id)
    df = pd.DataFrame(comments)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/video_comments.csv", index=False)