#  Парсер книжек #

При запуске кода скрипт скачивает книги и обложки к ним с сайта [tululu](https://tululu.org/) в формате __txt__. По умолчанию будут скачаны книги с 1-й по 701-ю страницу. По желанию пользователя может быть выбран другой диапазон. Также имеется возможность отказаться от скачивания либо текста книг, либо обложек, либо тех и других, и загружать только информацию о книгах в _json_ файл.

## Запуск

Для запуска бота у вас уже должен быть установлен __Python 3__.

###### **Настройка проекта**
- Скачайте код из репозитория github в отдельную папку.
- Установите зависимости командой `pip install -r requirements.txt`.
- Запустите скрипт командой `python3 main.py` 

## Примечание

Для облегчения работы со скриптом, можно использвать следующие команды, которые кобминируются друг с другом:

`python3 main.py --start_page *** --end_page ***` - выбор диапазона страниц
`python3 main.py --texts_folder ***` - выбор папки для сохранения текстов книг
`python3 main.py --imgs_folder ***` - выбор папки для сохранения обложек книг
`python3 main.py --json_path ***` - выбор папки для сохранения json-файла с информацией о книгах
`python3 main.py --skip_imgs` - команда для отказа от скачивания картинок
`python3 main.py --skip_texts` - команда для отказа от скачивания текстов

где _звездочки_ - это ваши значения.
