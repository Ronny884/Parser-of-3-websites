from parse_clinic import *
from parse_sushi import *
from parse_santaelena import *
from form_changer import *


if __name__ == '__main__':
    changer = FormChanger()

    clinics = ParseClinic('https://dentalia.com/', changer)
    clinics()
    sushi = ParseSushi('https://omsk.yapdomik.ru/', changer)
    sushi()
    candy_shop = ParseSantaElena('https://www.santaelena.com.co/', changer)
    candy_shop()
