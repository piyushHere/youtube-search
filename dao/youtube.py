from extensions import db
from models import Youtube
from sqlalchemy import desc



class YoutubeDAO(object):

    def commit(self):
        db.session.commit()

    def rollback(self):
        db.session.rollback()

    def close(self):
        db.session.close()

    def search_videos(self, query=""):
        allVideos = Youtube.query.filter(Youtube.title.ilike("%"+query+"%"), Youtube.desciption.ilike("%"+query+"%")).all()
        return allVideos

    def get_videos(self, page=0, offset=5):
        videos = db.session.query(Youtube).order_by(desc('publishing_datetime_ts')).paginate(
        page=page, per_page=offset,error_out=False,max_per_page=10
        )
        return videos
    
    def insert(self, video_mappings):
        for obj in video_mappings:
            youtube_row = Youtube(**obj)
            db.session.add(youtube_row)

