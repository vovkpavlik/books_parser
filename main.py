import os
from pprint import pprint

import requests
from urllib.parse import urljoin, urlsplit
import urllib3
from bs4 import BeautifulSoup
	
from pathvalidate import sanitize_filename
from urllib3.exceptions import HTTPError

import argparse


def check_for_redirect(response):
    if response.history:
        raise HTTPError


def download_txt(book_number, download_url, filename, folder="books/"):
    params = {"id":book_number}
    response = requests.get(download_url, params=params)
    response.raise_for_status()
    check_for_redirect(response)
    with open(f"{folder}{filename}.txt", "wb") as file:
        file.write(response.content)


def download_img(img_url, filename, folder="images/"):
    response = requests.get(img_url)
    response.raise_for_status()
    check_for_redirect(response)
    extension = os.path.splitext(urlsplit(img_url)[2])[-1]
    with open(f"{folder}{filename}{extension}", "wb") as file:
        file.write(response.content)    


def parse_book_page(book_url):
    response = requests.get(book_url)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')

    title_tag = soup.find(id="content").find("h1")
    title, author = title_tag.text.split("::") 

    genre_tag = soup.find("span", class_="d_book").find_all("a")
    genres = [genre.text for genre in genre_tag]

    comments_tag = soup.find_all(class_="texts")
    comments = [comment.find(class_="black").text for comment in comments_tag]

    img_tag = soup.find("div", class_="bookimage").find("img")["src"]
    img_url = urljoin(book_url, img_tag)

    book_info = {
        "Заголовок": sanitize_filename(title.strip()),
        "Автор": sanitize_filename(author.strip()),
        "Жанр": genres,
        "Комментарии": comments,
        "img_url": img_url
    }

    return book_info


def main():
    urllib3.disable_warnings()

    parser = argparse.ArgumentParser(description="Качает книжки с сайта тулулу")
    parser.add_argument('--start_id', help="стартовая страница", type=int)
    parser.add_argument('--end_id', help="конечная страница", type=int)
    args = parser.parse_args()

    os.makedirs("books/", exist_ok=True)
    os.makedirs("images/", exist_ok=True)

    for book_number in range(args.start_id, args.end_id):
        download_url = "https://tululu.org/txt.php"
        book_url = f"https://tululu.org/b{book_number}/"       
        try: 
            book_info = parse_book_page(book_url)
            img_url = book_info["img_url"]
            filename = f"{book_number}.{book_info['Заголовок']}"
            download_txt(book_number, download_url, filename)
            download_img(img_url, filename)
            # pprint(book_info)
            print()
            print()
        except HTTPError:
            print("Такой книги не существует в природе")


if __name__ == "__main__":
    main()
