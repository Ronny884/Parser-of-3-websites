import json
import requests
from bs4 import BeautifulSoup
from based_classes import *


class ParseClinic(StandardRequests, StandardParser):
    def __init__(self, base_url, changer):
        self.clinica_url = base_url + 'clinica/'
        self.changer = changer

    def __call__(self, *args, **kwargs):
        html_post = self.make_post_request()
        html_get = self.make_standard_get_request(self.clinica_url)
        soup_from_post = self.make_soup(html_post)
        soup_from_get = self.make_soup(html_get)
        name = self.make_list_of_clinic_names(soup_from_post)
        latlon = self.make_list_of_latlon(soup_from_get, count_of_clinics=len(name))
        address, phones, working_hours = self.make_lists_of_address_phones_and_working_hours(soup_from_post)
        finish_dictionary = self.make_finish_clinic_dict(name, address, latlon, phones, working_hours)
        return finish_dictionary

    def make_post_request(self):
        data = {
            'action': 'jet_engine_ajax',
            'handler': 'get_listing',
            'page_settings[post_id]': '5883',
            'page_settings[queried_id]': '344706|WP_Post',
            'page_settings[element_id]': 'c1b6043',
            'page_settings[page]': '1',
            'listing_type': 'elementor',
            'isEditMode': 'false',
        }
        response = requests.post(self.clinica_url, data=data)
        res = response.json()
        html = res['data']['html']
        return html

    @staticmethod
    def make_list_of_clinic_names(soup):
        name = []
        clinic_names_elements = soup.find_all('h3', attrs={'class': ['elementor-heading-title', 'elementor-size-default']})
        for clinic_name_element in clinic_names_elements:
            name.append(clinic_name_element.text)
        return name

    def make_lists_of_address_phones_and_working_hours(self, soup):
        address, phones, working_hours = [], [], []
        others_elements = soup.find_all('div', attrs={'class': ['jet-listing-dynamic-field__content']})
        for element in others_elements:
            some_data = element.text
            if 'Teléfono' in some_data:
                phones.append(self.changer.change_phone_form(some_data))
            elif 'Horario' in some_data:
                working_hours.append(self.changer.change_work_hours_form(some_data))
            else:
                address.append(some_data)
        return address, phones, working_hours

    @staticmethod
    def make_list_of_latlon(soup, count_of_clinics):
        latlon = []
        map_element = soup.find('div', attrs={'class': ['jet-map-listing', 'google-provider']})
        str_data = map_element.attrs['data-markers']
        json_data = json.loads(str_data)
        for i in range(count_of_clinics):
            coards = json_data[i]['latLang']
            latlon.append([coards['lat'], coards['lng']])
        return latlon

    @staticmethod
    def make_finish_clinic_dict(name, address, latlon, phones, working_hours):
        count_of_clinics = len(name)
        data = {'Сайт 1': []}
        for i in range(count_of_clinics):
            clinic = {'name': name[i],
                      'address': address[i],
                      'latlon': latlon[i],
                      'phones': phones[i],
                      'working_hours': working_hours[i]}
            data['Сайт 1'].append(clinic)
        return data









