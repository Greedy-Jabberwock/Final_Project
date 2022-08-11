from app import db
from app.models import Author, Genre, Book
from app.save_books_to_local import get_authors, get_books, UNZIP_FOLDER
import json


def populate_authors():
    authors = get_authors()
    for author in authors:
        if not Author.query.filter_by(fullname=author).first():
            new_record = Author(fullname=author)
            db.session.add(new_record)
            db.session.commit()
            print(f'{author} added to the db.')


def populate_genres():
    genres = ['novel', 'children', 'crime fiction', 'poetry', 'scientific',
              'humor', 'horror', 'other']
    for genre in genres:
        if not Genre.query.filter_by(genre=genre).first():
            new_record = Genre(genre=genre)
            db.session.add(new_record)
            db.session.commit()
            print(f'{genre.title()} added to the db.')


def populate_books():
    with open(fr'.\static\json\info.json', 'r') as f:
        books = json.load(f)
    for book in books:
        if Book.query.filter_by(title=book['title']).first():
            print(f'{book["title"]} already at the db.')
        else:
            new_record = Book(
                              title=book['title'],
                              description=book['description'],
                              release_year=book['copyright_year'],
                              total_time=book['totaltime'],
                              folder_name=book['folder_name'],
                              audio_path=book['audio_url'],
                              download_link=book['url_zip_file'],
                              image=book['image_url']
                              )
            db.session.add(new_record)

            new_record.genres.append(Genre.query.filter_by(genre=book['genre']).first())

            authors = book['authors'].split(', ')
            for author in authors:
                new_record.authors.append(Author.query.filter_by(fullname=author).first())

            db.session.add(new_record)
            db.session.commit()


def main():
    populate_authors()
    populate_genres()
    populate_books()


if __name__ == '__main__':
    main()
