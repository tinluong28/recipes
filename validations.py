from flask import flash
from models import User, Recipe, likes_table
import re
from datetime import date
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASS_REGEX = re.compile(r'^((?=.*\d)(?=.*[A-Z])(?=.*\W).{8,16})$')
NAME_REGEX = re.compile(r'^[a-zA-Z0-9_-]+$')


def calculateAge(birthdate):
    days_in_year = 365.2425
    bday_list = birthdate.split('-')
    bday = date(int(bday_list[0]), int(bday_list[1]), int(bday_list[2]))
    age = int((date.today() - bday).days / days_in_year)
    return age


def validate_signup(form):
    is_valid = True
    age = 0
    check_user_name = User.query.filter_by(user_name=form['user_name']).count()
    check_email = User.query.filter_by(email=form['email']).count()
    print(check_user_name)
    if form['birthdate']:
        age = calculateAge(form['birthdate'])
    if len(form['user_name']) < 1:
        is_valid = False
        flash('First name is required', 'errors')
    if not NAME_REGEX.match(form['user_name']):
        is_valid = False
        flash('User name should not contain any special characters', 'errors')
    if check_user_name > 0:
        is_valid = False
        flash('User name has been taken', 'errors')
    if check_email > 0:
        is_valid = False
        flash('This email has been registered', 'errors')
    if age < 18:
        is_valid = False
        flash('You must be at least 18 years old to register', 'errors')
    if len(form['password']) < 5:
        is_valid = False
        flash('Password should be at least 5 characters', 'errors')
    elif not PASS_REGEX.match(form['password']):
        is_valid = False
        flash('Password must contain at least a number and special character, upper and lowercase', 'errors')
    elif form['password'] != form['confirm_password']:
        is_valid = False
        flash('Confirm password must match with password', 'errors')
    if not EMAIL_REGEX.match(form['email']):
        is_valid = False
        flash("Invalid email address!", 'errors')
    if is_valid == False:
        return False
    if is_valid:
        return True


def validate_recipe(form):
    is_valid = True
    if len(form['name']) < 3:
        is_valid = False
        flash('Recipe name is required and must be at least 3 characters')
    if len(form['description']) < 3:
        is_valid = False
        flash('Recipe description is required and must be at least 3 characters')
    if len(form['instructions']) < 3:
        is_valid = False
        flash('Recipe instructions is required and must be at least 3 characters')
    if is_valid:
        return True
    else:
        return False
