import requests
from bs4 import BeautifulSoup
from based_classes import *


class ParseSantaElena(StandardRequests, StandardParser):
    def __init__(self, base_url, changer):
        self.base_url = base_url
        self.changer = changer

    def __call__(self, *args, **kwargs):
        html = self.make_standard_get_request(self.base_url)
        soup = self.make_soup(html)
        list_of_shop_location_urls = self.get_list_of_shop_location_urls(soup)
        names = self.find_all_names(list_of_shop_location_urls)
        finish_santa_elena_dict = self.make_finish_santa_elena_dict(names)
        return finish_santa_elena_dict

    @staticmethod
    def get_list_of_shop_location_urls(soup):
        """
        Блоки, содержащие информацию для разных локаций, находятся на разных url,
        которые также необходимо спарсить, чтобы обработать случай добавления новой
        локации и новых магазинов
        """
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

    def find_all_names(self, urls_list):
        """
        Совокупный список названий для всех локаций
        """
        all_names = []
        for url in urls_list:
            html = self.make_standard_get_request(url)
            soup = self.make_soup(html)
            names_of_location = self.find_names_of_location(soup)
            all_names += names_of_location
        return all_names

    def find_names_of_location(self, soup):
        """
        Находим названия магазинов для конкретной локации
        """
        name = []
        h3_elements = soup.find_all('h3', attrs={'class': ['elementor-heading-title',
                                                           'elementor-size-default']})
        for h3_element in h3_elements:
            name.append(self.changer.change_name_form(h3_element.text))
        return name

    @staticmethod
    def make_finish_santa_elena_dict(name, address=None, latlon=None, phones=None, working_hours=None):
        count_of_shops = len(name)
        data = {'Сайт 3': []}
        for i in range(count_of_shops):
            shop = {'name': name[i],
                    'address': address[i] if address is not None else '',
                    'latlon': latlon[i] if latlon is not None else [],
                    'phones': phones[i] if phones is not None else [],
                    'working_hours': working_hours[i] if working_hours is not None else []}
            data['Сайт 3'].append(shop)
        return data



