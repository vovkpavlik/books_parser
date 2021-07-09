import os

from pathlib import Path
import requests
import urllib3


def make_directory():
    directory = "books"
    import os
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def download_books():
    directory = make_directory()
    for book_number in range(10):
        url = f"https://tululu.org/txt.php?id={book_number}"
        filename = f"{directory}/book_{book_number}.txt"
        response = requests.get(url)
        response.raise_for_status()

        with open(filename, "wb") as file:
            file.write(response.content)


def main():
    urllib3.disable_warnings()
    download_books()



if __name__ == "__main__":
    main()