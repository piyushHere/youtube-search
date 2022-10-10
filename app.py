import config
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from clients.youtube import Youtube
from sqlalchemy import desc
import json
 

app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
youtube_client = Youtube()

class Youtube(db.Model):
    __tablename__ = 'youtube'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    desciption = db.Column(db.String())
    thumbnail_url = db.Column(db.String())
    publishing_datetime_ts = db.Column(db.DateTime(True), server_default=db.text("now()"))

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

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()