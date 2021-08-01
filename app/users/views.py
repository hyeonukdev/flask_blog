import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, current_app
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.users import users
from app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from app.users.models import User
from app import db


@users.route("/users")
def users_test():
    return render_template("users_test.html")


@users.route('/users/register', methods=['POST', 'GET'])
def register():
    """View for registration of new user"""

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(user_name=form.user_name.data, email=form.email.data,
                    age=form.age.data, university=form.university.data, department=form.department.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route('/users/login', methods=['POST', 'GET'])
def login():
    """View for login of existing user to the app"""

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.home')
            return redirect(next_page)
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route('/users/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/users/account", methods=['GET', 'POST'])
@login_required
def account():
    """View for Profile Page"""

    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.avatar.data:
            print(form.avatar.data)
            picture_file = save_avatar(form.avatar.data)
            current_user.avatar = picture_file
        current_user.user_name = form.user_name.data
        current_user.email = form.email.data
        current_user.age = form.age.data
        current_user.university = form.university.data
        current_user.department = form.department.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.user_name.data = current_user.user_name
        form.email.data = current_user.email
        form.age.data = current_user.age
        form.university.data = current_user.university
        form.department.data = current_user.department
    avatar = url_for('static', filename='avatar/' + current_user.avatar)
    return render_template('account.html', title='Account', form=form, avatar=avatar, projects=current_user.projects)


def save_avatar(form_picture):
    '''Function to save avatar into static/avatar directory with size optimization'''

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/avatar', picture_fn)

    output_size = (300, 300)    # avatar resizing
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn