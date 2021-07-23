import argparse
import os
from urllib.parse import urljoin, urlsplit, unquote
import json

import requests
import urllib3
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib3.exceptions import HTTPError

from parse_tululu_category import get_books_id


def check_for_redirect(response):
    if response.history:
        raise HTTPError


def download_txt(book_id, download_url, filename, folder):
    params = {"id":book_id}
    response = requests.get(download_url, params=params)
    response.raise_for_status()
    check_for_redirect(response)
    with open (f"{os.path.join(folder, filename)}.txt", "w") as file:
        file.write(response.text)


def download_img(img_url, filename, folder):
    response = requests.get(img_url)
    response.raise_for_status()
    check_for_redirect(response)
    _, extension = os.path.splitext(urlsplit(unquote(img_url)).path)
    with open (f"{os.path.join(folder, filename)}{extension}", "wb") as file:
        file.write(response.content)    


def parse_book_page(book_url):
    response = requests.get(book_url) 
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')

    title_tag = soup.select_one("#content h1")
    title, author = title_tag.text.split("::") 

    genres = [
        genre.text for genre in
        soup.select("span.d_book a")
    ]

    comments = [
        comment.text for comment in
        soup.select(".texts .black")
    ]

    img_src = soup.select_one(".bookimage img")["src"]
    img_url = urljoin(book_url, img_src)

    book_info = {     
        "title": title.strip(),
        "author": author.strip(),
        "genre": genres,
        "comments": comments,
        "img_url": img_url    
    }

    return book_info


def main():
    urllib3.disable_warnings()

    parser = argparse.ArgumentParser(description="Качает книжки с сайта тулулу")
    parser.add_argument("--start_page", default=1, help="стартовая страница", type=int)
    parser.add_argument("--end_page", default=701, help="конечная страница", type=int)
    parser.add_argument("--texts_folder", default="books_texts", help="путь к текстам книг", type=str)
    parser.add_argument("--imgs_folder", default="books_images", help="путь к картинкам книг", type=str)
    parser.add_argument("--json_path", default=os.getcwd(), help="путь к json файлу с информацией о книгах", type=str)
    parser.add_argument("--skip_imgs", action="store_true", help="отменяет загрузку картинок")
    parser.add_argument("--skip_texts", action="store_true", help="отменяет загрузку текстов")
    args = parser.parse_args()

    books_info = []

    books_id = get_books_id(args.start_page, args.end_page) 
 
    for book_id in books_id:
        download_url = "https://tululu.org/txt.php" 
        book_url = f"https://tululu.org/b{book_id}/"       
        
        try: 
            book_info = parse_book_page(book_url) 
            books_info.append(parse_book_page(book_url))
            img_url = book_info["img_url"]
            book_title = f"{book_id}.{book_info['title']}"
            filename = sanitize_filename(book_title)
            
            if not args.skip_imgs:
                os.makedirs(args.imgs_folder, exist_ok=True)
                download_img(img_url, filename, args.imgs_folder)
            if not args.skip_texts:
                os.makedirs(args.texts_folder, exist_ok=True)
                download_txt(book_id, download_url, filename, args.texts_folder)

        except HTTPError:
            print("Такой книги не существует в природе")

    if args.json_path:
       os.makedirs(args.json_path, exist_ok=True) 
    with open(os.path.join(args.json_path, "books_info.json"), "a") as my_file:
        json.dump(
            books_info, 
            my_file, 
            sort_keys=True, 
            indent=4, 
            ensure_ascii=False
        )


if __name__ == "__main__":
    main()
