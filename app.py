import config, atexit, json
from flask import Flask, request, abort
from flask_migrate import Migrate
from clients.youtube import YoutubeClient
from apscheduler.schedulers.background import BackgroundScheduler
from extensions import db

youtube_client = YoutubeClient()
 

app = Flask(__name__)
app.config.from_object(config.Config)
db.init_app(app)

from services.youtube import YoutubeService
youtube_service = YoutubeService()
migrate = Migrate(app, db)

def youtube_cron_job():
    """Run scheduled job."""
    with app.app_context():
        print("Fetching data from youtube")
        youtube_service.fetch_youtube()
        print("Stored data fetched from youtube")


cron = BackgroundScheduler()
cron.add_job(func=youtube_cron_job, trigger="interval", seconds=10)
cron.start()

@app.route("/youtube_data")
def get_youtube_data():
    try:
        data = youtube_service.get_youtube_data()
        return json.dumps(data)
    except Exception as e:
        print("something went wrong with the server", e)
        abort(500, e)

@app.route("/search")
def search_youtube_data():
    try:
        data = youtube_service.search_youtube_data()
        return json.dumps(data)
    except Exception as e:
        print("something went wrong with the server", e)
        abort(500, e)


atexit.register(lambda: cron.shutdown(wait=False))

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host="0.0.0.0", port=5000)