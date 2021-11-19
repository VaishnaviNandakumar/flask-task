import os
import pymongo
from dotenv import load_dotenv
from googleapiclient.discovery import build
from flask import Flask, render_template, request
import time
from functools import wraps
from threading import Thread


#Set up configuration 
load_dotenv()
api_key = os.environ['API_KEY']
client = pymongo.MongoClient(os.environ['MONGO_CONNECTION_STRING'])
db = client['YOUTUBE']
collection = db['music_videos']
collection.ensure_index([
      ('description', 'text'),
      ('title', 'text'),
  ],
  name="search_index",
  weights={
      'title':100,
      'description':25
  }
)
app = Flask(__name__, template_folder="templates", static_folder='../static')

def fetchData():
    print("Fetching Videos..")
    interrupted = False
    while True:
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.search().list(
                part='snippet',
                q='vlogs',
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
            #Prevents repetition of videos
            count =  collection.count_documents({'videoID': dataObject['videoID']})
            if count == 0:
                collection.insert_one(dataObject)
        time.sleep(10)

@app.route('/')
def main():
    return "Hello World"

@app.route('/videos', methods=['GET'])
def getData():
    data = collection.find().sort([("publishedAt", pymongo.DESCENDING)])
    keyset = ['videoID','title','description','publishedAt','thumbnail','channel']
    return render_template("videolist.html", data_list=data, keyset=keyset)

@app.route('/search', methods=['GET','POST'])
def searchData():
    if request.method == "POST":
        query = request.form.get('query')
        #text_results = db.command('text', 'music_videos', search=query)
        doc_matches = collection.find({"$text": {"$search": query}})
        print(doc_matches)
        keyset = ['videoID','title','description','publishedAt','thumbnail','channel']
        return render_template("search.html", search_results=doc_matches, keyset=keyset, documents=1)
    else:
        return render_template("search.html", search_results=[], keyset=[], documents=0)


if __name__ == "__main__":
    app.secret_key =  os.environ['SECRET_KEY']
    thread = Thread(target=fetchData)
    #thread.daemon = True
    #thread.start()
    app.run()