import requests
from bs4 import BeautifulSoup
from based_classes import *


class ParseSushi(StandardRequests, StandardParser):
    def __init__(self, base_url, changer):
        self.omsk_url_about = base_url + 'about'
        self.changer = changer

    def __call__(self, *args, **kwargs):
        html = self.make_standard_get_request(self.omsk_url_about)
        soup = self.make_soup(html)
        phones = self.parse_phones(soup)
        address = self.parse_address(soup)
        finish_sushi_dict = self.make_finish_sushi_dict(address, phones)
        return finish_sushi_dict

    @staticmethod
    def parse_phones(soup):
        div_phone = soup.find('div', attrs={'class': 'contacts__phone'})
        phones_element = div_phone.find('a', attrs={'class': ['link', 'link--black', 'link--underline']})
        phones = [phones_element.text.replace(" ", "")]
        return phones

    @staticmethod
    def parse_address(soup):
        address = []
        parent = soup.find('div', attrs={'class': 'site-footer__address-list'})
        address_elements = parent.find_all('li')
        for address_element in address_elements:
            address.append(address_element.text)
        return address

    @staticmethod
    def make_finish_sushi_dict(address, phones, name=None, latlon=None, working_hours=None):
        count_of_sushi_houses = len(address)
        data = {'Сайт 2': []}
        for i in range(count_of_sushi_houses):
            shop = {'name': name[i] if name is not None else 'Японский домик',
                    'address': 'Омск, ' + address[i],
                    'latlon': latlon[i] if latlon is not None else [],
                    'phones': phones,
                    'working_hours': working_hours[i] if working_hours is not None else []}
            data['Сайт 2'].append(shop)
        return data









