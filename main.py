import json
from parse_clinic import *
from parse_sushi import *
from parse_santaelena import *
from form_changer import *


if __name__ == '__main__':
    changer = FormChanger()
    # clinics = ParseClinic('https://dentalia.com/', changer)
    # sushi = ParseSushi('https://omsk.yapdomik.ru/', changer)
    candy_shop = ParseSantaElena('https://www.santaelena.com.co/', changer)
    # clinics = clinics()
    # sushi = sushi()
    candy = candy_shop()
    # result_dict = clinics | sushi | candy
    result_dict = candy
    result_json = json.dumps(result_dict, ensure_ascii=False)
    print(result_json)

