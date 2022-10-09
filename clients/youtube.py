from urllib.parse import urljoin
import requests
from os import environ, path
from dotenv import load_dotenv
import datetime


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

API_HOST = environ.get('YOUTUBE_HOST')
API_KEY = environ.get('YOUTUBE_DATA_V3_KEY')

class Youtube():
    def __init__(self):
        self.api_host = API_HOST
        self.search_api = "youtube/v3/search"
        self.api_key = API_KEY

    def get_search_response(self):
        url = urljoin(
            self.api_host, self.search_api
        )
        params = {
            'part': 'snippet',
            'key': self.api_key,
            'publishedAfter': (datetime.datetime.now() - datetime.timedelta(weeks=1)).isoformat() + 'Z',
            'type': 'video',
            'order': 'date'
        }
        response = requests.get(url, params)
        return response.json()
            