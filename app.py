import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
api_key = os.environ['API_KEY']
youtube = build('youtube', 'v3', developerKey=api_key)
request = youtube.search().list(
        part='snippet',
        q='music videos',
        type='video'
    )
response = request.execute()
resultList = response['items']
for result in resultList:
    entry = result['snippet']
    dataObject = {}
    dataObject['title'] = entry['title']
    dataObject['description'] = entry['description']
    dataObject['publishedAt'] = entry['publishedAt']
    dataObject['thumbnail'] = entry['thumbnails']['default']['url']
    dataObject['channel'] = entry['channelTitle']
    print("Data Object : ", dataObject)
    
