import os
import time
import json
import requests
from bs4 import BeautifulSoup
from based_classes import *


class ParseSantaElena(StandardRequests, StandardParser, MakerJSON):
    def __init__(self, base_url, changer):
        self.base_url = base_url
        self.changer = changer

    def __call__(self, *args, **kwargs):
        html = self.make_standard_get_request(self.base_url)
        soup = self.make_soup(html)
        list_of_shop_location_urls = self.get_list_of_shop_location_urls(soup)
        print(list_of_shop_location_urls)

    @staticmethod
    def get_list_of_shop_location_urls(soup):
        a = soup.find_all('a', attrs={'href': 'https://www.santaelena.com.co/tiendas-pasteleria/',
                                      'class': "elementor-item",
                                      'tabindex': "-1"})[0]
        parent_of_a = a.find_parent()
        list_of_li_elements = parent_of_a.find_all('li')
        location_urls = []
        for li_element in list_of_li_elements:
            child_of_li_element = li_element.find('a')
            location_url = child_of_li_element.attrs['href']
            location_urls.append(location_url)
        return location_urls

