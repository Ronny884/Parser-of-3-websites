import re


class FormChanger:
    @staticmethod
    def change_phone_form(phones):
        phone_pattern = re.compile(r"\(\d+\) *[0-9 \-]+")
        phone_list = phone_pattern.findall(phones)
        res_list = [phone.strip() for phone in phone_list]
        return res_list

    @staticmethod
    def change_work_hours_form(input_string):
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


