import streamlit as st
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import pandas as pd

from etl.video_etl import etl_video_data
from etl.comment_etl import load_comments_to_csv

st.set_page_config(page_title="YouTube Data Engineering App", page_icon=":movie_camera:", layout="wide")
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_channel_id(youtube, channel_name):
    req = youtube.search().list(q=channel_name, type='channel', part='id', maxResults=1)
    res = req.execute()
    items = res.get('items')
    if items:
        return items[0]['id']['channelId']
    return None

def get_video_ids(youtube, channel_id, max_results=50):
    req = youtube.search().list(channelId=channel_id, part='id', maxResults=max_results, order='date', type='video')
    res = req.execute()
    return [item['id']['videoId'] for item in res.get('items', [])]

def get_video_metadata(youtube, video_ids):
    if not video_ids:
        return []
    req = youtube.videos().list(part="snippet", id=','.join(video_ids))
    res = req.execute()
    data = []
    for item in res.get('items', []):
        snippet = item['snippet']
        data.append({
            'video_id': item['id'],
            'title': snippet['title'],
            'thumbnail_url': snippet['thumbnails']['medium']['url']
        })
    return data

def show_home():
    st.markdown(
        """
        <div style='text-align:center; margin-bottom: 1.5em;'>
            <span style='font-size:3em;'>🎬</span>
            <h1 style='margin-bottom:0.2em;'>YouTube Data Engineering App</h1>
            <p style='font-size:1.2em; color:gray;'>Extract, Transform, and Download YouTube Video & Comment Data Easily</p>
        </div>
        """, unsafe_allow_html=True
    )
    if "channel_name" not in st.session_state:
        st.session_state.channel_name = ""
    if "videos" not in st.session_state:
        st.session_state.videos = []
    if "channel_id" not in st.session_state:
        st.session_state.channel_id = None

    channel_name = st.text_input("Search YouTube Channel", value=st.session_state.channel_name, help="Enter YouTube Channel you want")
    col1, col2 = st.columns([1, 1])
    with col1:
        search_btn = st.button("Search", use_container_width=True)
    with col2:
        reset_btn = st.button("Reset", use_container_width=True)

    if reset_btn:
        st.session_state.channel_name = ""
        st.session_state.videos = []
        st.session_state.channel_id = None
        st.rerun()

    if search_btn and channel_name:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        channel_id = get_channel_id(youtube, channel_name)
        if channel_id:
            video_ids = get_video_ids(youtube, channel_id)
            videos = get_video_metadata(youtube, video_ids)
            st.session_state.channel_name = channel_name
            st.session_state.channel_id = channel_id
            st.session_state.videos = videos
        else:
            st.warning("Channel not found.")

    if st.session_state.videos:
        st.markdown("<h3 style='text-align:center;'>Video's Result</h3>", unsafe_allow_html=True)
        cols = st.columns(2)
        if "playing_video_id" not in st.session_state:
            st.session_state.playing_video_id = None
        for idx, video in enumerate(st.session_state.videos):
            with cols[idx % 2]:
                if st.session_state.playing_video_id == video['video_id']:
                    st.video(f"https://www.youtube.com/watch?v={video['video_id']}")
                    if st.button("🔙 Back to Thumbnail", key=f"back_thumb_{video['video_id']}", use_container_width=True):
                        st.session_state.playing_video_id = None
                        st.rerun()
                else:
                    st.markdown(
                        f"""
                        <div style='text-align:center; margin-bottom:1em; border:1px solid #eee; border-radius:12px; padding:1em; background:rgba(255,255,255,0);'>
                            <img src="{video['thumbnail_url']}" width="320" style="border-radius:8px;"/>
                            <h6 style='margin:0.5em 0 0.7em 0; min-height:4em; display:flex; align-items:center; justify-content:center;'>{video['title']}</h6>
                        """, unsafe_allow_html=True
                    )
                    if st.button("▶️ Play", key=f"play_{video['video_id']}", use_container_width=True):
                        st.session_state.playing_video_id = video['video_id']
                        st.rerun()
                    col_btn1, col_btn2 = st.columns([1,1])
                    with col_btn1:
                        if st.button("🎥 Get Video Data", key=f"get_video_{video['video_id']}", use_container_width=True):
                            with st.spinner("Processing ETL Video Data..."):
                                etl_video_data([video['video_id']])
                            st.session_state.page = "video_data"
                            st.rerun()
                    with col_btn2:
                        if st.button("💬 Get Comment Data", key=f"get_comment_{video['video_id']}", use_container_width=True):
                            with st.spinner("Processing ETL Comment Data..."):
                                load_comments_to_csv(video['video_id'])
                            st.session_state.page = "comment_data"
                            st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

def show_video_data_page():
    st.markdown("<h2 style='text-align:center;'>📊 ETL Video Data Result</h2>", unsafe_allow_html=True)
    if os.path.exists("data/videos_metadata.csv"):
        df = pd.read_csv("data/videos_metadata.csv")
        st.dataframe(df.head())
        st.download_button("Download CSV", df.to_csv(index=False), file_name="videos_metadata.csv", mime="text/csv")
    else:
        st.info("Video data not found. Please perform ETL first.")
    if st.button("⬅️ Back to Home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

def show_comment_data_page():
    st.markdown("<h2 style='text-align:center;'>💬 ETL Comment Data Result</h2>", unsafe_allow_html=True)
    if os.path.exists("data/video_comments.csv"):
        df = pd.read_csv("data/video_comments.csv")
        st.dataframe(df.head())
        st.download_button("Download CSV", df.to_csv(index=False), file_name="video_comments.csv", mime="text/csv")
    else:
        st.info("Comment data not found. Please perform ETL first.")
    if st.button("⬅️ Back to Home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

def main():
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if st.session_state.page == "home":
        show_home()
    elif st.session_state.page == "video_data":
        show_video_data_page()
    elif st.session_state.page == "comment_data":
        show_comment_data_page()

if __name__ == "__main__":
    main()