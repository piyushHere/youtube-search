import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
 

app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Youtube(db.Model):
    __tablename__ = 'youtube'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    desciption = db.Column(db.String())
    thumbnail_url = db.Column(db.String())
    publishing_datetime_ts = db.Column(db.DateTime(True), server_default=db.text("now()"))

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(port=8000, debug=True)