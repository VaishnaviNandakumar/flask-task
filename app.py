import os
import pymongo
from dotenv import load_dotenv
from googleapiclient.discovery import build
from flask import Flask
import time
from functools import wraps
import threading
import atexit

#Set up configuration 
load_dotenv()
api_key = os.environ['API_KEY']
client = pymongo.MongoClient(os.environ['MONGO_CONNECTION_STRING'])
db = client['YOUTUBE']
collection = db['music_videos']


app = Flask(__name__, template_folder="../templates", static_folder='../static')

def fetchData():
    print("Here")
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
        dataObject['videoID'] = result['id']['videoId']
        dataObject['title'] = entry['title']
        dataObject['description'] = entry['description']
        dataObject['publishedAt'] = entry['publishedAt']
        dataObject['thumbnail'] = entry['thumbnails']['default']['url']
        dataObject['channel'] = entry['channelTitle']
        collection.insert_one(dataObject)

@app.route('/')
def main():
    return "Hello World"

if __name__ == "__main__":
    app.secret_key =  os.environ['SECRET_KEY']
    app.run()