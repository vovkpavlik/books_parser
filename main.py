import os

from pathlib import Path
import requests
import urllib3
from urllib3.exceptions import HTTPError


def make_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def check_for_redirect(redirect):
    if not redirect:
        pass
    else:
        raise HTTPError


def main():
    urllib3.disable_warnings()
    
    folder = make_directory("books")

    for book_number in range(10):
        response = requests.get(f"https://tululu.org/txt.php?id={book_number}")
        response.raise_for_status()
        try:
            check_for_redirect(response.history)
            filename = f"{folder}/book_{book_number}.txt"
            with open(filename, "wb") as file:
                file.write(response.content)
        except HTTPError: 
            print("Такой книги не существует в природе")


if __name__ == "__main__":
    main()
