import requests
from bs4 import BeautifulSoup
from based_classes import *


class ParseSushi(RequestsMaker, StandardParser):
    def __init__(self, base_url, changer):
        self.omsk_url_about = base_url + 'about'
        self.changer = changer

    def __call__(self, *args, **kwargs):
        html = self.make_standard_get_request(self.omsk_url_about).content
        soup = self.make_soup(html)
        phones = self.parse_phones(soup)
        addresses = self.parse_address(soup)
        latlons = self.get_latlons(addresses)
        working_hours = self.get_working_hours('Японский домик', addresses)
        finish_sushi_dict = self.make_finish_sushi_dict(addresses=addresses,
                                                        phones=phones,
                                                        latlons=latlons,
                                                        working_hours=working_hours)
        return finish_sushi_dict

    @staticmethod
    def parse_phones(soup):
        """
        На данном сайте для всех заведений Омска указан только один номер
        """
        div_phone = soup.find('div', attrs={'class': 'contacts__phone'})
        phones_element = div_phone.find('a', attrs={'class': ['link', 'link--black', 'link--underline']})
        phones = [phones_element.text.replace(" ", "")]
        return phones

    @staticmethod
    def parse_address(soup):
        addresses = []
        parent = soup.find('div', attrs={'class': 'site-footer__address-list'})
        address_elements = parent.find_all('li')
        for address_element in address_elements:
            addresses.append('Омск, ' + address_element.text)
        return addresses

    def get_latlons(self, addresses):
        latlons = []
        for address in addresses:
            response = self.make_request_for_coards_getting(address).json()
            latlon = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
            latlons.append([latlon.replace(' ', ', ')])
        return latlons

    def get_working_hours(self, org_name, addresses):
        working_hours_list = []
        for address in addresses:
            response = self.make_request_for_working_hours_getting(org_name, address).json()
            working_hours = response['features'][0]['properties']['CompanyMetaData']['Hours']['text']
            working_hours_changed = self.changer.change_working_hours_string_for_sushi(working_hours)
            working_hours_list.append([working_hours_changed])
        return working_hours_list

    @staticmethod
    def make_finish_sushi_dict(addresses, phones, latlons, working_hours):
        count_of_sushi_houses = len(addresses)
        data = {'Сайт 2': []}
        for i in range(count_of_sushi_houses):
            shop = {'name': 'Японский домик',  # у всех ресторанов одно название
                    'address': addresses[i],
                    'latlon': latlons[i],
                    'phones': phones,
                    'working_hours': working_hours[i]}
            data['Сайт 2'].append(shop)
        return data
