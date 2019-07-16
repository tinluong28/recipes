from flask import render_template, request, redirect, flash, session
from config import db
from models import User, Recipe, likes_table


def test():
    return 'Ready for build'
