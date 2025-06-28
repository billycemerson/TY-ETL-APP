from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

# Load .env file from parent directory (src)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_youtube_service():
    return build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def search_channels(query):
    youtube = get_youtube_service()
    response = youtube.search().list(
        q=query,
        type='channel',
        part='id,snippet',
        maxResults=5
    ).execute()
    return response.get('items', [])

def get_channel_videos(channel_id):
    youtube = get_youtube_service()
    response = youtube.search().list(
        channelId=channel_id,
        part='id,snippet',
        maxResults=50,
        order='date'
    ).execute()
    return response.get('items', [])

def get_video_details(video_ids):
    youtube = get_youtube_service()
    response = youtube.videos().list(
        part='snippet,statistics',
        id=','.join(video_ids)
    ).execute()
    return response.get('items', [])

def get_video_comments(video_id):
    youtube = get_youtube_service()
    comments = []
    page_token = ''
    while True:
        response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            pageToken=page_token,
            maxResults=100,
            textFormat='plainText'
        ).execute()
        comments.extend(response.get('items', []))
        page_token = response.get('nextPageToken')
        if not page_token:
            break
    return comments