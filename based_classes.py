import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup


class RequestsMaker:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3'}

    def make_standard_get_request(self, url):
        response = requests.get(url, headers=self.headers)
        return response

    @staticmethod
    def make_standard_post_request(url, data):
        response = requests.post(url, data)
        return response

    def make_request_for_coards_getting(self, address):
        """
        Получение координат с помощью API Геокодера (Яндекс)
        """
        load_dotenv()
        api_key = os.getenv('API_KEY_1')
        url = f'https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&geocode={address}&format=json'
        response = self.make_standard_get_request(url)
        return response

    def make_request_for_working_hours_getting(self, org_name, address):
        """
        Получение времени работы заведения с помощью API Поиска по организациям (Яндекс)
        """
        load_dotenv()
        api_key = os.getenv('API_KEY_2')
        text = org_name + ' ' + address
        url = f'https://search-maps.yandex.ru/v1/?text={text}&type=biz&lang=en_US&apikey={api_key}'
        response = self.make_standard_get_request(url)
        return response


class StandardParser:
    @staticmethod
    def make_soup(content):
        soup = BeautifulSoup(content, 'html.parser')
        return soup



