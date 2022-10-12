from dao.youtube import YoutubeDAO
from clients.youtube import YoutubeClient
from flask import request


class YoutubeService(object):
    def __init__(self) -> None:
        self.youtube_dao = YoutubeDAO()
        self.youtube_client = YoutubeClient()
    
    def get_youtube_data(self):
        page = request.args.get('page', 0, type=int)
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
    
    def fetch_youtube(self):
        response = self.youtube_client.get_search_response()
        response = self.get_response_items_dict(response)
        self.youtube_dao.insert(response)
        self.youtube_dao.commit()
        self.youtube_dao.close()

    def get_response_items_dict(self, response):
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

