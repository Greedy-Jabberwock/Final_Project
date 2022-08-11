import os
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Book, Genre
from app import db

main_bp = Blueprint('main_bp', __name__)


@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/home', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', type=int, default=1)
    books = Book.query.paginate(page=page, per_page=6)
    genres = Genre.query.all()

    return render_template('main/index.html', books=books, genres=genres)


@main_bp.route('/details/<book_id>')
def details(book_id):
    book = Book.query.filter_by(id=book_id).first()
    authors_str = ', '.join(x.fullname for x in book.authors)
    return render_template('main/details.html', book=book, authors=authors_str)


@main_bp.route('/genre/<genre>', methods=["GET", "POST"])
def genre_page(genre):
    genres = Genre.query.all()
    current_genre = Genre.query.filter_by(genre=genre).first()
    books = current_genre.books

    return render_template('main/genre_page.html', genres=genres, books=books, genre=genre)


@main_bp.route('/profile/', methods=["GET"])
@login_required
def profile():
    return render_template('main/profile.html', books=current_user.bookshelf.books)


@main_bp.route('/add_book/<book_id>', methods=['POST'])
@login_required
def add_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if book in current_user.bookshelf.books:
        flash('This book is already on your bookshelf.', 'info')
    else:
        current_user.bookshelf.books.append(book)
        db.session.commit()
        flash('Book added to your bookshelf!', 'success')
    return redirect(url_for('main_bp.details', book_id=book_id))


@main_bp.route('/delete_book/<book_id>')
@login_required
def delete_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    current_user.bookshelf.books.remove(book)
    db.session.commit()
    return redirect(url_for('main_bp.profile'))


@main_bp.route('/listen_book/<book_id>')
@login_required
def listening(book_id):
    book = Book.query.filter_by(id=book_id).first()
    audio_list = (url_for('static', filename=f'audio/{book.folder_name}/{x}') for x in os.listdir(book.audio_path))
    return render_template('main/listen_page.html', book=book, test=audio_list)


@main_bp.route('/about')
def about():
    return render_template('main/about.html')


