## Парсер вебсайтов
Проект представляет из себя скрипт, собирающий информацию с 3 сайтов и сохраняющий её в json с определённой структурой.
Сайты, с которых собирается информация:
1) https://dentalia.com/
2) https://omsk.yapdomik.ru/
3) https://www.santaelena.com.co/

Работа ведётся с помощью requests, bs4. Для сохранения данных в правильном виде используются регулярные выражения.
Так же в проекте реализовано подключение к API Геокодера (Яндекс) и API Поиска по организациям (Яндекс) для сбора
геоданных и информации о времени работы заведений (в случае, если с сайта данную информацию спарсить невозможно).
