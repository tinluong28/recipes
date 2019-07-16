from flask import render_template, request, redirect, flash, session
from config import db, bcrypt
from models import User, Recipe, likes_table
from validations import validate_signup
from datetime import datetime


def index():
    return render_template('index.html')


def register():
    is_valid = validate_signup(request.form)
    if is_valid:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        new_instance_of_user = User(user_name=request.form['user_name'], email=request.form['email'],
                                    location=request.form['location'], hashed_pw=pw_hash, birthdate=request.form['birthdate'])
        db.session.add(new_instance_of_user)
        db.session.commit()
        flash('Registered successfully!! Please sign in', 'success')
    else:
        flash('Unsuccessful. Please try again', 'errors')
    return redirect('/')


def login():
    user = User.query.filter_by(user_name=request.form['user_name']).first()
    if user:
        if bcrypt.check_password_hash(user.hashed_pw, request.form['password']):
            session['userID'] = user.id
            return redirect('/dashboard')
    flash('You could not be logged in. Try agian!', 'login error')
    return redirect('/')


def dashboard():
    return render_template('dashboard.html')
