import config
from flask import Flask, request
from flask_migrate import Migrate
from clients.youtube import Youtube
youtube_client = Youtube()
from sqlalchemy import desc
import json
 

app = Flask(__name__)
app.config.from_object(config.Config)
from models import db, Youtube
migrate = Migrate(app, db)


@app.cli.command()
def scheduled():
    """Run scheduled job."""
    print("Fetching data from youtube")
    fetch_youtube()
    print("Stored data fetched from youtube")

def get_response_items_dict(response):
    items = response["items"]
    response_list = []
    for item in items:
        response_list.append({
            "title": item["snippet"]["title"],
            "desciption": item["snippet"]["description"],
            "publishing_datetime_ts": item["snippet"]["publishTime"],
            "thumbnail_url": item["snippet"]["thumbnails"]["default"]["url"]
        })
    return response_list

def insert_into_db(response):
    for obj in response:
        youtube_row = Youtube(**obj)
        db.session.add(youtube_row)
    db.session.commit()
    db.session.close()

def fetch_youtube():
    response = youtube_client.get_search_response()
    response = get_response_items_dict(response)
    insert_into_db(response)

@app.route("/youtube_data")
def get_youtube_data():
    page = request.args.get('page', 1, type=int)
    offset = request.args.get('offset', 5, type=int)
    response = []
    objects = db.session.query(Youtube).order_by(desc('publishing_datetime_ts')).paginate(
        page=page, per_page=offset,error_out=False,max_per_page=10
        )
    for obj in objects:
        response.append({
            "title": obj.title
        })
    return json.dumps(response)

@app.route("/search")
def search_youtube_data():
    response = []
    query = request.args.get("query") # here query will be the search inputs name
    allVideos = Youtube.query.filter(Youtube.title.ilike("%"+query+"%"), Youtube.desciption.ilike("%"+query+"%")).all()
    for video in allVideos:
        response.append({
            "title": video.title,
            "description": video.desciption
        })
    return json.dumps(response)

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()