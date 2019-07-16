from sqlalchemy.sql import func
from config import db

likes_table = db.Table('likes',
                       db.Column('user_id', db.Integer, db.ForeignKey(
                           'user.id'), primary_key=True),
                       db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    location = db.Column(db.String(45), nullable=False)
    hashed_pw = db.Column(db.String(60), nullable=False)
    birthdate = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now())
    recipes_this_user_likes = db.relationship('Recipes', secondary=likes_table)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', foreign_keys=[
                             author_id], backref='recipes', cascade='all', lazy=True)
    users_who_like_this_recipe = db.relationship('User', secondary=likes_table)
