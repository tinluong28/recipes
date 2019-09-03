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
        recipes = Recipe.query.filter_by().count()
        user_recipes = Recipe.query.filter_by(
            author_id=session['userID']).count()
        return render_template('dashboard.html', user=user, all_recipes=recipes, user_recipes=user_recipes)
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
                name=request.form['name'], description=request.form['description'], instructions=request.form['instructions'], ingredients=request.form['ingredients'], under30=request.form['under30'], author_id=session['userID'])
            db.session.add(new_instance_of_recipe)
            db.session.commit()
            return redirect('/review')
    else:
        return redirect('/')


def review():
    if session['userID']:
        user = User.query.get(session['userID'])
        recipes = Recipe.query.all()
        liked_recipes = []
        for recipe in user.recipes_this_user_likes:
            liked_recipes.append(recipe.id)
        return render_template('review.html', user=user, recipes=recipes, liked_recipes=liked_recipes)
    else:
        return redirect('/')


def all_users_review():
    if session['userID']:
        user = User.query.get(session['userID'])
        recipes = Recipe.query.all()
        # put liked recipes' ID in an array
        liked_recipes = []
        for recipe in user.recipes_this_user_likes:
            liked_recipes.append(recipe.id)
        return render_template('all_users_review.html', user=user, recipes=recipes, liked_recipes=liked_recipes)
    else:
        return redirect('/')


def display_instruction(recipe_id):
    if session['userID']:
        user = User.query.get(session['userID'])
        recipe = Recipe.query.get(recipe_id)
        liked_recipes = []
        been_liked = False
        for recipe_user_liked in user.recipes_this_user_likes:
            liked_recipes.append(recipe_user_liked.id)
            if recipe_user_liked.id == recipe.id:
                been_liked = True
        # instructions = recipe.instructions.split(".")
        return render_template('display_instruction.html', user=user, recipe=recipe, liked_recipes=liked_recipes, been_liked=been_liked)
    else:
        return redirect('/')


def like_recipe():
    if session['userID']:
        recipe_id = request.form['recipe_id']
        current_recipe = Recipe.query.get(recipe_id)
        current_user = User.query.get(session['userID'])
        current_user.recipes_this_user_likes.append(current_recipe)
        db.session.commit()
        # return render_template('partials/liked_msg.html', liked=True, recipe=current_recipe)
        return redirect('/instruction/{}'.format(recipe_id))
    else:
        return redirect('/')


def unlike_recipe():
    if session['userID']:
        recipe_id = request.form['recipe_id']
        current_recipe = Recipe.query.get(recipe_id)
        current_user = User.query.get(session['userID'])
        current_user.recipes_this_user_likes.remove(current_recipe)
        db.session.commit()
        # return render_template('partials/liked_msg.html', unliked=True, recipe=current_recipe)
        return redirect('/instruction/{}'.format(recipe_id))
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
        return render_template('partials/username.html', too_short=True, user_name=True)
    else:
        found = False
        username = User.query.filter_by(
            user_name=request.form['user_name']).first()
        if username:
            found = True
        return render_template('partials/username.html', too_short=False, user_name=True, user_found=found)


def verify_email():
    email = User.query.filter_by(email=request.form['email']).first()
    if email:
        email_found = True
        return render_template('partials/email.html', email_found=True)
    else:
        return render_template('partials/email.html', email_found=False)

def logout():
    session.clear()
    return redirect('/')
