import requests
from bs4 import BeautifulSoup


class StandardRequests:
    @staticmethod
    def make_standard_get_request(url):
        response = requests.get(url)
        return response.content


class StandardParser:
    @staticmethod
    def make_soup(content):
        soup = BeautifulSoup(content, 'html.parser')
        return soup



