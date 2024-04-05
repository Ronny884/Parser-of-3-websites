import os
import time
import json
import requests
from bs4 import BeautifulSoup
from based_classes import *


class ParseSushi(StandardRequests, StandardParser, MakerJSON):
    def __init__(self, base_url, changer):
        self.omsk_url_about = base_url + 'about'
        self.changer = changer

    def __call__(self, *args, **kwargs):
        html = self.make_standard_get_request(self.omsk_url_about)
        soup = self.make_soup(html)
        phones = self.parse_phones(soup)
        # address = self.parse_address(soup)

    def make_response_for_html(self):
        headers = {
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'Referer': 'https://omsk.yapdomik.ru/',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
        }
        response = requests.get('https://storage.yandexcloud.net/softdel/assets/js/app.345448.js', headers=headers)
        print(response.text)
        return response.content

    @staticmethod
    def parse_phones(soup):
        div_phone = soup.find('div', attrs={'class': 'contacts__phone'})
        phones_element = div_phone.find('a', attrs={'class': ['link', 'link--black', 'link--underline']})
        phones = [phones_element.text.replace(" ", "")]
        return phones

    def parse_address(self, soup):
        address = []







