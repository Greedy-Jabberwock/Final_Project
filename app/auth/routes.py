from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, logout_user, login_required, login_user
from app.auth.forms import SignUp, Login, RequestResetPassword, ResetPassword
from app.auth.functions import sign_up_user, log_in_user, send_reset_email
from app.models import User

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))

    signup_form = SignUp()
    if signup_form.validate_on_submit():
        user = sign_up_user(signup_form.username.data,
                            signup_form.email.data,
                            signup_form.password.data)
        if user:
            login_user(user)
            return redirect(url_for('main_bp.index'))
        else:
            flash('This username or email already taken.')
    return render_template('auth/signup.html', form=signup_form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))

    login_form = Login()
    if login_form.validate_on_submit():
        user = log_in_user(login_form.username.data, login_form.password.data)
        if user:
            login_user(user)
            return redirect(url_for('main_bp.index'))
        else:
            flash('Invalid username or password.', 'warning')

    return render_template('auth/login.html', form=login_form)


@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))


@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))

    request_reset_form = RequestResetPassword()
    if request_reset_form.validate_on_submit():
        send_reset_email(request_reset_form.email.data)
        flash('An email with instructions has been sent.', 'success')
        return redirect(url_for('auth_bp.login'))

    return render_template('auth/reset_request.html', form=request_reset_form)


@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))

    user = User.verify_reset_password_token(token)
    if not user:
        flash('The token invalid or expired.', 'warning')
        return redirect(url_for('auth_bp.reset_password'))

    reset_form = ResetPassword()
    if reset_form.validate_on_submit():
        reset_password(user, reset_form.password.data)
        flash('Your password successfully changed. You can login now.', 'success')
        return redirect(url_for('auth_bp.login'))

    return render_template('auth/reset_token.html', form=reset_form)
