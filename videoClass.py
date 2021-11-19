from config import *

class Video:
    def fetchData(self):
        print("Fetching Videos..")
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

    def get(self):
        data = collection.find().sort([("publishedAt", pymongo.DESCENDING)])
        keyset = ['videoID','title','description','publishedAt','thumbnail','channel']
        return render_template("videolist.html", data_list=data, keyset=keyset)

    def search(self):
        if request.method == "POST":
            query = request.form.get('query')
            doc_matches = collection.find({"$text": {"$search": query}})
            keyset = ['videoID','title','description','publishedAt','thumbnail','channel']
            return render_template("search.html", search_results=doc_matches, keyset=keyset, documents=1)
        else:
            return render_template("search.html", search_results=[], keyset=[], documents=0)
