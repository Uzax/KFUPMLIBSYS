from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, login_required, current_user
from __init__ import db

auth = Blueprint('auth', __name__) 

@auth.route('/login', methods=['GET', 'POST']) 
def login(): 
    if request.method=='GET': 
        return render_template('login.html')
    else: 
        username = request.form.get('username')
        password = request.form.get('password')
       
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(username = username).first()
       
        if not user:
            flash('Please sign up before!')
            return redirect(url_for('auth.signup'))
        elif user.password != password:
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup(): 
    if request.method=='GET': 
        return render_template('signup.html')
    else: 
        email = request.form.get('email')
        username = request.form.get('name')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first() 
        if user: 
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))


        new_user = User(username=username, email=email, password=password) #
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

@auth.route('/logout') # define logout path
@login_required
def logout(): #define the logout function
    logout_user()
    return redirect(url_for('main.index'))