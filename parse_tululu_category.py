import requests
from urllib.parse import urljoin, urlsplit
from bs4 import BeautifulSoup


def get_books_id(url):   
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    
    books_href = [
        book.find("td").find("a")["href"] for book in
        soup.find(id="content").find_all("table")
    ]
    
    books_url = [urljoin("https://tululu.org", book) for book in books_href]
  
    books_id = []
    for book_url in books_url:
        _, book_id = (urlsplit(book_url).path).split("b")
        books_id.append(book_id.rstrip("/"))

    return books_id
