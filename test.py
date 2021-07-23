import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

book_url = "https://tululu.org/b9/"
response = requests.get(book_url)

response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')

genres = [
    genre.text for genre in
    soup.find("span", class_="d_book").find_all("a")
]

genres_2 = [
    genre.text for genre in
    soup.select("span.d_book a")
]

comments = [
    comment.find("span", class_="black").text for comment in
    soup.find_all("div", class_="texts")
]

comments_2 = soup.select("div.texts span.black")
comments_3 = [
    comment.text for comment in
    soup.select("div.texts span.black")
]

print(comments)
print(comments_3)