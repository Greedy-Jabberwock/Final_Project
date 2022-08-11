from app import login_manager, db, mail, bcrypt
from app.models import User, BookShelf
from flask_mail import Message
from flask import url_for
import os


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


def sign_up_user(username, email, password):
    new_user = User(username=username, email=email, password=bcrypt.generate_password_hash(password).decode('utf-8'))
    db.session.add(new_user)
    new_bookshelf = BookShelf(owner=new_user)
    db.session.add(new_bookshelf)
    db.session.commit()
    return new_user


def log_in_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return user


def send_reset_email(email):
    user = User.query.filter_by(email=email).first()
    token = user.get_reset_password_token()
    msg = Message('Password Reset Request',
                  sender=os.environ.get('MAIL_USER'),
                  recipients=[user.email])
    msg.body = f'''Visit the link to reset your password:
{url_for('auth_bp.reset_token', token=token, _external=True)}
    
If you didn't make this request, ignore this message.
    '''
    mail.send(msg)


def reset_password(user, password):
    user.password = password
    db.session.commit()
