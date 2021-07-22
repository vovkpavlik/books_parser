import requests
from urllib.parse import urljoin, urlsplit
from bs4 import BeautifulSoup


def get_books_url(start_page, end_page):     
    books_url = []
    for page in range(start_page, end_page):
        url = f"https://tululu.org/l55/{page}"

        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        books_href = [
            book.find("td").find("a")["href"] for book in
            soup.find(id="content").find_all("table")
        ]
       
        one_page_books_url = [urljoin("https://tululu.org", book) for book in books_href]

        books_url.extend(one_page_books_url)
    
    return books_url
    

def get_books_id(start_page, end_page):
    books_id = []
    books_url = get_books_url(start_page, end_page)
    for book_url in books_url:
        _, book_id = (urlsplit(book_url).path).split("b")
        books_id.append(book_id.rstrip("/"))
    
    return books_id
