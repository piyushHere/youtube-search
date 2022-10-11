from dao.youtube import YoutubeDAO
from flask import request


class YoutubeService(object):
    def __init__(self) -> None:
        self.youtube_dao = YoutubeDAO()
    
    def get_youtube_data(self):
        page = request.args.get('page', 1, type=int)
        offset = request.args.get('offset', 5, type=int)
        response = []
        objects = self.youtube_dao.get_videos(page, offset)
        for obj in objects:
            response.append({
                "title": obj.title
            })
        return response

    def search_youtube_data(self):
        response = []
        query = request.args.get("query") # here query will be the search inputs name
        allVideos = self.youtube_dao.search_videos(query=query)
        for video in allVideos:
            response.append({
                "title": video.title,
                "description": video.desciption
            })
        return response

