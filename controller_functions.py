from flask import render_template, request, redirect, flash, session
from config import db, bcrypt
from models import User, Recipe, likes_table
from validations import validate_signup, validate_recipe
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
    if session['userID']:
        user = User.query.get(session['userID'])
        return render_template('dashboard.html', user=user)
    else:
        return redirect('/')


def create():
    if session['userID']:
        user = User.query.get(session['userID'])
        return render_template('create.html', user=user)
    else:
        return redirect('/')


def create_recipe():
    if session['userID']:
        if validate_recipe(request.form):
            new_instance_of_recipe = Recipe(
                name=request.form['name'], description=request.form['description'], instructions=request.form['instructions'], under30=request.form['under30'], author_id=session['userID'])
            db.session.add(new_instance_of_recipe)
            db.session.commit()
            return redirect('/review')


def review():
    if session['userID']:
        user = User.query.get(session['userID'])
        recipes = Recipe.query.all()
        print(recipes)
        return render_template('review.html', user=user, recipes=recipes)
    else:
        return redirect('/')


def display_instruction(recipe_id):
    if session['userID']:
        user = User.query.get(session['userID'])
        recipe = Recipe.query.get(recipe_id)
        return render_template('display_instruction.html', user=user, recipe=recipe)
    else:
        return redirect('/')


def delete_recipe(recipe_id):
    if session['userID']:
        recipe = Recipe.query.get(recipe_id)
        print(recipe.__dict__)
        db.session.delete(recipe)
        db.session.commit()
        return redirect('/review')
    else:
        return redirect('/')


def verify_username():
    if len(request.form['user_name']) < 3:
        found = False
        username = User.query.filter_by(
            user_name=request.form['user_name']).first()
        if username:
            found = True
        return render_template('partials/username.html', user_name=True, user_found=found)


def verify_email():
    found = False
    email = User.query.filter_by(email=request.form['email']).first()
    if email:
        found = True
    return render_template('/partials/username.html', email=True, email_found=found)


def logout():
    session.clear()
    return redirect('/')
