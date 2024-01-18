from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_user
from flask import request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')

        user = User.query.filter_by(username=username).first()
        if (user):
            if (check_password_hash(password, user.password)):
                flash('Password is incorrect!', category='failure')
            else:
                login_user(user, remember=remember)
                return redirect(url_for('views.home'))
        else:
            flash('User does not exist', category='failure')


    return render_template('login.html', user=current_user)

@auth.route('/sign-up', methods=['GET','POST'])
def signUp():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')
        remember = request.form.get('remember')

        userByUsername = User.query.filter_by(username=username).first()
        userByEmail = User.query.filter_by(email=email).first()

        if userByEmail:
            flash('Email already in use', category='failure')
        elif userByUsername:
            flash('Username already taken', category='failure')
        elif (len(email) > 200):
            flash('Email cannot be greater than 200 characters', category='failure')
        elif (len(username) > 200):
            flash('Username cannot be greater than 200 characters', category='failure')
        elif (len(firstName) > 200):
            flash('First name cannot be greater than 200 characters', category='failure')
        elif (len(lastName) > 200):
            flash('Last name cannot be greater than 200 characters', category='failure')
        elif (password != confirmPassword):
            flash('Passwords do not match!', category='failure')
        else:
            new_user = User(email=email, username=username, firstName=firstName, lastName=lastName, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=remember)
            return redirect(url_for('views.home'))

    return render_template('sign-up.html',user=current_user)

