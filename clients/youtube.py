import requests
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

API_HOST = environ.get('https://youtube.googleapis.com')
API_KEY = environ.get('YOUTUBE_DATA_V3_KEY')

class Youtube():
    def __init__(self):
        self.api_host = API_HOST
        self.search_api = "youtube/v3/search"
        self.api_key = API_KEY
    

    def get_search_response(self):
        response = requests.get()
        if 500 <= response.status_code < 600:
            error_msg = 'Youtube api not responding'
            