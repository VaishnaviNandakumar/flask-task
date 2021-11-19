from config import *
from videoClass import Video

app = Flask(__name__, template_folder="templates", static_folder='static')

@app.route('/')
def main():
    return render_template("home.html")

@app.route('/videos', methods=['GET'])
def getData():
    return Video().get()


@app.route('/search', methods=['GET','POST'])
def searchData():
    return Video().search()

if __name__ == "__main__":
    app.secret_key =  os.environ['SECRET_KEY']
    thread = Thread(target=Video().fetchData)
    #thread.start()
    app.run()