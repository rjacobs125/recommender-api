import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging
import requests


logger = logging.getLogger(__name__)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()


def search_youtube_tutorials(tool_name):
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        logger.error("🚨 YOUTUBE_API_KEY not set.")
        return None

    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.search().list(
            q=f"{tool_name} tutorial",
            part='snippet',
            maxResults=1,
            type='video'
        )
        response = request.execute()

        tutorials = []
        for item in response.get('items', []):
            video_id = item['id']['videoId']
            link = f"https://www.youtube.com/watch?v={video_id}"
            tutorials.append(link)

        return tutorials

    except HttpError as e:
        logger.error(f"🚨 YouTube API error: {e}")
        return None  # fallback to default
    except Exception as e:
        logger.error(f"🚨 Unexpected error in search_youtube_tutorials: {e}")
        return None  # fallback to default