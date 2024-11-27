import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
load_dotenv()

api_key = os.getenv("YOUTUBE_API_KEY")

def get_video_details(video_id: str):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.videos().list(part='snippet', id=video_id)
    response = request.execute()
    return response['items'][0]['snippet']['description']

def search_video(keyword: str):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(q=keyword, part="id", type='video', maxResults=1)
    response = request.execute()

    if response["items"]:
        return response['items'][0]['id']['videoId']
    else:
        return None

