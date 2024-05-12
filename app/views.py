from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from . import app, db
from .forms import LanguageForm, LoginForm, RegistrationForm
from .models import Languages, User


@app.route('/')
def index():
    language_list = Languages.query.order_by(Languages.created_date).all()
    return render_template('index.html',
                           languages=language_list[::-1])


@app.route('/language_detail/<int:id>')
def language_detail(id):
    languages = Languages.query.get(id)
    return render_template('language_detail.html',
                           languages=languages)


@app.route('/add_language', methods=['GET', 'POST'])
@login_required
def add_language():
    form = LanguageForm()
    if form.validate_on_submit():
        languages = Languages()
        languages.title = form.title.data
        languages.text = form.text.data
        db.session.add(languages)
        db.session.commit()
        return redirect(url_for('language_detail', id=languages.id))
    return render_template('add_language.html',
                           form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Вход выполнен!', 'alert-success')
            return redirect(url_for('index'))
        else:
            flash('Вход не выполнен!', 'alert-danger')
    return render_template('login.html', form=form)


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.name = form.name.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно!', 'alert-success')
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
