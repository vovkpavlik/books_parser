from pprint import pprint
import json

book_info_1 = {
    "title": "1",
    "author": "2",
    "genre": "3",
    "comments": "4",
    "img_url": "5"
}

book_info_2 = {
    "title": "a",
    "author": "b",
    "genre": "c",
    "comments": "d",
    "img_url": "e"
}

books_info = []
books_info.append(book_info_1)
books_info.append(book_info_2)
pprint(books_info)


with open("books_info.json", "a") as my_file:
    json.dump(
        books_info, 
        my_file, 
        sort_keys=True, 
        indent=4, 
        ensure_ascii=False
    )