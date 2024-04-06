import re
from datetime import datetime


class FormChanger:
    @staticmethod
    def change_name_form(name):
        name = name.strip()
        name = name.replace('  ', ' ')
        name = name.replace('\n', ' ')
        return name

    @staticmethod
    def change_phone_form(phones):
        phone_pattern = re.compile(r"\(\d+\) *[0-9 \-]+")
        phone_list = phone_pattern.findall(phones)
        res_list = [phone.strip() for phone in phone_list]
        return res_list

    @staticmethod
    def change_clinic_work_hours_form(input_string):
        input_string = input_string.replace('Horario: ', '')
        input_string = input_string.replace('\r\n', ' ')
        input_string = input_string.replace(' a ', '-')
        replacements = {
            'L': 'mon',
            'M': 'tue',
            'J': 'thu',
            'V': 'fri',
            'S': 'sat',
            'D': 'sun'
        }
        output_string = ''
        repeated_M = False
        for char in input_string:
            if char in replacements:
                if char == 'M' and repeated_M:
                    output_string += 'Wed'
                else:
                    output_string += replacements[char]
                    if char == 'M':
                        repeated_M = True
            else:
                output_string += char

        return [output_string.strip()]

    @staticmethod
    def change_working_hours_string_for_sushi(time_str):
        time_match = re.search(r'\d{1,2}:\d{2}\s*[APap][Mm]–\d{1,2}:\d{2}\s*[APap][Mm]', time_str)
        extracted_time = time_match.group()
        start_time, end_time = extracted_time.split('–')
        start_time_24h = datetime.strptime(start_time.strip(), '%I:%M %p').strftime('%H:%M')
        end_time_24h = datetime.strptime(end_time.strip(), '%I:%M %p').strftime('%H:%M')
        result_str = 'Пн - Вс ' + f"{start_time_24h} - {end_time_24h}"
        return result_str

    @staticmethod
    def remove_contained_strings(input_list):
        result_list = input_list.copy()
        for i, outer_string in enumerate(input_list):
            for j, inner_string in enumerate(input_list):
                if i != j and inner_string in outer_string:
                    result_list.remove(inner_string)
                    break
        return result_list

    @staticmethod
    def change_structure_of_list_of_shops_data(list):
        """
        Метод принимает список из списков, каждый из которых соответствует
        конкретному одному магазину. Данные списки могут содержать 2, 3 или 4 строки.

        2 строки: требуется добавить в середину списка список ['-'], что свидетельствует
        о том, что номер для магазина на сайте отсутствует.Последнюю строку помещаем в список
        3 строки: строки номера и часов работы поместить в списки, если две последние строки не
        разделённые части режима работы. В противном случае объединяем и делаем так же,
        как и в случае двух строк
        4 строки: две последние строки оъединить в один список, номер также поместить в список
        5 строк: две первые строки составляют адрес. Объединяем их
        """
        if len(list) == 2:
            list[1] = [list[1]]
            list.insert(1, ['-'])

        elif len(list) == 3:
            if 'Lunes a Sábado' in list[1]:
                item_2 = [list[1], list[2]]
                list.pop()
                list.pop()
                list.append(item_2)
                list.insert(1, ['Not on the site'])
            else:
                list[1] = [list[1]]
                list[2] = [list[2]]

        elif len(list) == 4:
            list[1] = [list[1]]
            item_3 = [list[2], list[3]]
            list.pop()
            list.pop()
            list.append(item_3)

        else:
            item_0 = list[0] + list [1]
            list.pop(0)
            list.pop(0)
            list.insert(0, item_0)

            list[1] = [list[1]]
            item_3 = [list[2], list[3]]
            list.pop()
            list.pop()
            list.append(item_3)
        return list

    @staticmethod
    def get_last_words_from_list(string_list):
        last_words = []
        for string in string_list:
            words = string.split()
            last_words.append(words[-1])
        return last_words


