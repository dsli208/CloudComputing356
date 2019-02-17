from flask import render_template, request, Blueprint
import time
# from flaskr.db import get_db
# from app import app
from app import ttt_app

ttt = Blueprint('ttt', __name__, url_prefix='/ttt/')

@ttt_app.route('/', methods=['POST'], endpoint='/ttt/play/')

def get_name():
    if request.method == 'POST':
        name = request.form['name']
        if not name:
            error = 'Name is required.'

        return greeting(name)

def simple_greeting():
    return "Hello world!"

def greeting(name):
    return "Hello" + name + "," + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())

# @ttt_app.route('/ttt/', methods=['POST'], endpoint='/ttt/play/')