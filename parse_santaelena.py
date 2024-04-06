import requests
from bs4 import BeautifulSoup
from based_classes import *


class ParseSantaElena(RequestsMaker, StandardParser):
    def __init__(self, base_url, changer):
        self.base_url = base_url
        self.changer = changer

    def __call__(self, *args, **kwargs):
        html = self.make_standard_get_request(self.base_url).content
        soup = self.make_soup(html)
        list_of_shop_location_urls = self.get_list_of_shop_location_urls(soup)
        list_of_cities = self.make_list_of_corresponding_cities(soup)
        combo_data = self.start_find_loop_for_each_location(list_of_shop_location_urls, list_of_cities)
        latlons = self.get_latlons(combo_data)
        names, other_data, cities = combo_data[0], combo_data[1], combo_data[2]
        finish_santa_elena_dict = self.make_finish_santa_elena_dict(names=names, latlons=latlons,
                                                                    other_data=other_data, cities=cities)
        return finish_santa_elena_dict

    @staticmethod
    def get_list_of_shop_location_urls(soup):
        """
        Блоки, содержащие информацию для разных локаций, находятся на разных url,
        которые также необходимо спарсить, чтобы обработать случаи добавления
        новых магазинов в новые локации
        """
        a = soup.find_all('a', attrs={'href': 'https://www.santaelena.com.co/tiendas-pasteleria/',
                                      'class': "elementor-item",
                                      'tabindex': "-1"})[0]
        parent_of_a = a.find_parent()
        list_of_li_elements = parent_of_a.find_all('li')
        location_urls = []
        list_of_links_texts = []
        for li_element in list_of_li_elements:
            child_of_li_element = li_element.find('a')
            list_of_links_texts.append(child_of_li_element.text)
            location_url = child_of_li_element.attrs['href']
            location_urls.append(location_url)
        return location_urls

    def make_list_of_corresponding_cities(self, soup):
        """
        Список городов, соответствующих url-адресам, необходим для последующего
        составления полного адреса каждого магазина
        """
        a = soup.find_all('a', attrs={'href': 'https://www.santaelena.com.co/tiendas-pasteleria/',
                                      'class': "elementor-item",
                                      'tabindex': "-1"})[0]
        parent_of_a = a.find_parent()
        list_of_li_elements = parent_of_a.find_all('li')
        list_of_links_texts = []
        for li_element in list_of_li_elements:
            child_of_li_element = li_element.find('a')
            list_of_links_texts.append(child_of_li_element.text)
        list_of_city_names = self.changer.get_last_words_from_list(list_of_links_texts)
        return list_of_city_names

    def start_find_loop_for_each_location(self, urls_list, list_of_cities):
        """
        Запускаем цикл, что проводит поиск необходимых данных в каждой
        из локаций(город), попутно вызывая необходимые методы
        """
        all_names = []
        all_other_data = []
        sequence_of_cities = []
        for url, city in zip(urls_list, list_of_cities):
            html = self.make_standard_get_request(url).content
            soup = self.make_soup(html)

            names_of_location = self.find_names_for_location(soup)
            parent_elements_of_location = self.make_list_of_relevant_parent_elements_for_location(soup)
            combo_list_of_other_data = self.find_all_texts_in_relevant_parent_element(parent_elements_of_location)

            for i in range(len(combo_list_of_other_data)):
                sequence_of_cities.append(city)

            all_names += names_of_location
            all_other_data += combo_list_of_other_data
        data = (all_names, all_other_data, sequence_of_cities)
        return data

    def find_names_for_location(self, soup):
        """
        Поиск всех необходимых названий магазинов в рамках одной локации (города)
        """
        names = []
        h3_elements = soup.find_all('h3', attrs={'class': ['elementor-heading-title',
                                                           'elementor-size-default']})
        for h3_element in h3_elements:
            names.append(self.changer.change_name_form(h3_element.text))
        return names

    def make_list_of_relevant_parent_elements_for_location(self, soup):
        """
        Создадим список всех элементов класса 'elementor-text-editor elementor-clearfix',
        которые содержат в себе теги <p> или <h4> (суммарно) в количестве не менее 2
        и не содержат ссылок <a>
        В результате получим список элементов, наследники которых содержат
        всю актуальную информацию для каждого магазина
        """
        primary_list = soup.find_all('div', attrs={'class': ['elementor-text-editor', 'elementor-clearfix']})
        finish_list = []
        for element in primary_list:
            p_elements = element.find_all('p')
            h4_elements = element.find_all('h4')
            a_elements = element.find_all('a')
            count = len(p_elements) + len(h4_elements)
            if count >= 2 and a_elements == []:
                finish_list.append(element)
        return finish_list

    def find_all_texts_in_relevant_parent_element(self, list_of_parent_elements):
        """
        Каждый элемент (из прошлого методо) содержит информацию под разными тегами.
        Чтобы её получить, требуется скомпановать все текстовые надписи, содеращиеся
        в элементах, в виде строк внутри списков
        """
        list_of_shops_data_for_one_location = []
        unnecessary_strings = ('Dirección:', 'Dirección',
                               'Teléfono:', 'Teléfono',
                               'Horario de atención:',
                               'Horario de atención',
                               '  ', ' ', '', ' ')
        for parent_element in list_of_parent_elements:
            list_of_texts_for_one_shop = []
            all_child_elements = parent_element.find_all()
            for child_element in all_child_elements:
                text = child_element.text
                if text not in unnecessary_strings:
                    list_of_texts_for_one_shop.append(text)
            list_of_texts_for_one_shop = self.changer.remove_contained_strings(list_of_texts_for_one_shop)
            list_of_texts_for_one_shop = self.changer.change_structure_of_list_of_shops_data(list_of_texts_for_one_shop)
            list_of_shops_data_for_one_location.append(list_of_texts_for_one_shop)
        return list_of_shops_data_for_one_location

    def get_latlons(self, combo_data):
        """
        Получаем координаты с помощью API Геокодера (Яндекс)
        """
        latlons = []
        addresses = []
        for i in range(len(combo_data[0])):
            address = combo_data[2][i] + ' ' + combo_data[1][i][0]
            addresses.append(address)
        for address in addresses:
            response = self.make_request_for_coards_getting(address[0:25]).json()
            latlon = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
            latlons.append([latlon.replace(' ', ', ')])
        return latlons

    @staticmethod
    def make_finish_santa_elena_dict(names, latlons, other_data, cities):
        count_of_shops = len(names)
        data = {'Сайт 3': []}
        for i in range(count_of_shops):
            shop = {'name': names[i],
                    'address': cities[i] + ' ' + other_data[i][0],
                    'latlon': latlons[i],
                    'phones': other_data[i][1],
                    'working_hours': other_data[i][2]}
            data['Сайт 3'].append(shop)
        return data



