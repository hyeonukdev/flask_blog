from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from app.users import users
from app import db
from app.users.forms import RegistrationForm, LoginForm
from app.users.models import User
from werkzeug.urls import url_parse


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
                    age=form.age.data, address=form.address.data)
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