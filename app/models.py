import app
from app import db
from flask_login import UserMixin
from time import time
import jwt

# ====================== Assertion tables ============================


bookshelf_book = db.Table('bookshelf_book',
                          db.Column('bookshelf_id', db.Integer, db.ForeignKey('bookshelfs.id')),
                          db.Column('book_id', db.Integer, db.ForeignKey('books.id'))
                          )

book_author = db.Table('book_author',
                       db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
                       db.Column('author_id', db.Integer, db.ForeignKey('authors.id'))
                       )

book_genre = db.Table('book_genre',
                      db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
                      db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'))
                      )


# =========================== Models =================================


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    """
    User table represents username, hashed email and hashed password.
    
    Relationships:
    - Bookshelf (1:1)
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    bookshelf = db.relationship('BookShelf', backref='owner', uselist=False)

    def get_reset_password_token(self, expires_in=600):
        timeout = time() + expires_in
        payload = {
            'reset_password': self.id,
            'exp': timeout
        }

        secret_key = app.Config.SECRET_KEY
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        return token

    @staticmethod
    def verify_reset_password_token(token):
        try:
            user_id = jwt.decode(token, app.Config.SECRET_KEY,
                                 algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(user_id)


class BookShelf(db.Model):
    __tablename__ = 'bookshelfs'

    """
    Bookshelf table represents collection of books of specified user.
    
    Relationships:
    - User (1:1)
    - Book (M:M)
    """

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    books = db.relationship('Book', secondary='bookshelf_book', backref='in_bookshelfs')


class Book(db.Model):
    __tablename__ = 'books'

    """
    Book table represents all information about the book
    
    Relationships:
    - Bookshelf (M:M)
    - Author (M:M)
    - Genre (M:M)
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    release_year = db.Column(db.String, nullable=False)
    total_time = db.Column(db.String, nullable=False)
    audio_path = db.Column(db.String, nullable=False)
    folder_name = db.Column(db.String)
    download_link = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    authors = db.relationship('Author', secondary='book_author', backref='books')
    genres = db.relationship('Genre', secondary='book_genre', backref='books')


class Author(db.Model):
    __tablename__ = 'authors'
    """
    Authors table represents authors
    
    Relationships:
    - Book (M:M)
    """

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String, nullable=False)


class Genre(db.Model):
    __tablename__ = 'genres'

    """
    Genres table represents genres names
    
    Relationships:
    - Book (M:M)
    """

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String, nullable=False)

