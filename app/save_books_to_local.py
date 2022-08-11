import json
import os

import requests
import xmltodict
import pyunpack


ZIP_FOLDER = r'Z:\DI\Books\books\zips'
UNZIP_FOLDER = r"app\static\audio"


def get_books():
    """
    Get all books from librivox API in xml format, reformat data into Python dictionary.

    :return: all_books_list
    """

    all_books_list = list()
    params = {'fields': '{title,description,copyright_year,authors,genres,sections,url_zip_file,totaltime}'}
    response = requests.get(r'https://librivox.org/api/feed/audiobooks/', params=params)
    if response.status_code == 200:
        response_dict = json.loads(json.dumps(xmltodict.parse(response.content)))
        books = response_dict['xml']['books']['book']
        for book in books:
            book_dict = dict()
            for key, value in book.items():
                book_dict[key] = value
            all_books_list.append(book_dict)
        for book in all_books_list:
            book['folder_name'] = ''.join(tuple(filter(lambda _: _.isalpha(), book['title'])))
            book['audio_url'] = fr'{UNZIP_FOLDER}\{book["folder_name"]}'

            book['image_url'] = 'img_here'

            if isinstance(book['authors']['author'], list):
                full_names = []
                for _ in book['authors']['author']:
                    first_name = f'{_["first_name"]}'.strip().replace('None', '')
                    last_name = f' {_["last_name"]}'.strip().replace('None', '')
                    full_names.append(f'{first_name}{last_name}'.strip())
                book['authors'] = ', '.join(full_names)
            else:
                book['authors'] = f"{book['authors']['author']['first_name']} {book['authors']['author']['last_name']}"
        all_books_list = sorted(all_books_list, key=lambda _: _['folder_name'])

        return all_books_list


def get_authors():
    """
    Get all authors from librivox API.

    :return: all_authors: list of fullnames
    """

    all_authors = set()
    params = {'fields': '{authors}', 'format': 'json'}
    response = requests.get(r'https://librivox.org/api/feed/audiobooks/', params=params)
    response = json.loads(response.content)
    for book in response['books']:
        if isinstance(book['authors'], list):
            for author in book['authors']:
                all_authors.add(f'{author["first_name"].strip()} {author["last_name"].strip()}')
        else:
            element = book['authors']
            all_authors.add(f'{element["first_name"].strip()} {element["last_name"].strip()}')
    all_authors = sorted(list(all_authors))
    return all_authors


def save_zip_to_local(all_books):
    """
    Get zip files from librivox API and save them to local machine. If folder is not empty - pass.

    :param all_books: list of books
    :return: None
    """
    if not os.listdir(ZIP_FOLDER):
        for book in all_books:
            response = requests.get(book['url_zip_file'])
            with open(fr'{ZIP_FOLDER}\{book["folder_name"]}.zip', 'wb') as local_file:
                local_file.write(response.content)
            print(f'{book["folder_name"]} was added to zips folder')
    else:
        print('Zips folder already up to date.')


def unpack_zips(books):
    """
    Unpack saved zip files from librivox API to local folder. If folder is not empty - pass.

    :param books: list
    :return: None
    """
    if not os.listdir(UNZIP_FOLDER):
        for book in books:
            unzip_book_folder = rf'{UNZIP_FOLDER}\{book["folder_name"]}'
            os.mkdir(unzip_book_folder)
            pyunpack.Archive(rf'{ZIP_FOLDER}\{book["folder_name"]}.zip').extractall(unzip_book_folder)
    else:
        print('Unzips folder already up to date.')


def save_data_json(all_books):
    """
    Create json file with data of books

    :param all_books:
    :return: None
    """
    with open(fr'app\static\json\info.json', 'w') as json_file:
        json.dump(all_books, json_file, indent=4)
        print('JSON written')


def main():
    all_books = get_books()
    save_zip_to_local(all_books)
    unpack_zips(all_books)
    save_data_json(all_books)


if __name__ == '__main__':
    main()
