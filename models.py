from extensions import db


class Youtube(db.Model):
    __tablename__ = 'youtube'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    desciption = db.Column(db.String())
    thumbnail_url = db.Column(db.String())
    publishing_datetime_ts = db.Column(db.DateTime(True), server_default=db.text("now()"))