import argparse
import os
from urllib.parse import urljoin, urlsplit, unquote

import requests
import urllib3
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib3.exceptions import HTTPError

from parse_tululu_category import get_books_id


def check_for_redirect(response):
    if response.history:
        raise HTTPError


def download_txt(book_id, download_url, filename, folder="books"):
    params = {"id":book_id}
    response = requests.get(download_url, params=params)
    response.raise_for_status()
    check_for_redirect(response)
    with open (f"{os.path.join(folder, filename)}.txt", "w") as file:
        file.write(response.text)


def download_img(img_url, filename, folder="images"):
    response = requests.get(img_url)
    response.raise_for_status()
    check_for_redirect(response)
    _, extension = os.path.splitext(urlsplit(unquote(img_url)).path)
    with open (f"{os.path.join(folder, filename)}{extension}", "wb") as file:
        file.write(response.content)    


def get_books_url(page_url):   
    response = requests.get(page_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    
    books_href = [
        book.find("td").find("a")["href"] for book in
        soup.find(id="content").find_all("table")
    ]
    
    books_url = [urljoin("https://tululu.org", book) for book in books_href]
  
    return books_url


def parse_book_page(book_url):
    response = requests.get(book_url)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')

    title_tag = soup.find(id="content").find("h1")
    title, author = title_tag.text.split("::") 

    genres = [
        genre.text for genre in
        soup.find("span", class_="d_book").find_all("a")
    ]

    comments = [
        comment.find("span", class_="black").text for comment in
        soup.find_all("div", class_="texts")
    ]

    img_src = soup.find("div", class_="bookimage").find("img")["src"]
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
    parser.add_argument('--start_id', default=1, help="стартовая страница", type=int)
    parser.add_argument('--end_id',default=11, help="конечная страница", type=int)
    args = parser.parse_args()

    os.makedirs("books", exist_ok=True)
    os.makedirs("images", exist_ok=True)

    fantastic_genre_url = "https://tululu.org/l55/"
    books_id = get_books_id(fantastic_genre_url)
    for page in range(args.start_id, args.end_id+1):
        fantastic_genre_url = f"https://tululu.org/l55/{page}"
        books_id = get_books_id(fantastic_genre_url)
        for book_id in books_id:
            download_url = "https://tululu.org/txt.php" 
            book_url = f"https://tululu.org/b{book_id}/"       
            try:
                print(parse_book_page(book_url))
                book_info = parse_book_page(book_url)
                img_url = book_info["img_url"]
                book_title = f"{book_id}.{book_info['title']}"
                filename = sanitize_filename(book_title)
                # download_txt(book_id, download_url, filename)
                # download_img(img_url, filename)
            except HTTPError:
                print("Такой книги не существует в природе")


if __name__ == "__main__":
    main()
