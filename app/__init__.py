import pymongo
from random import randint
import json

from flask import Flask, render_template, request, url_for, jsonify, redirect, flash
from flask_mail import Mail, Message
from flask_pymongo import PyMongo

ttt_app = Flask(__name__)

ttt_app.config['MAIL_SERVER']='smtp.gmail.com'
ttt_app.config['MAIL_PORT'] = 587
ttt_app.config['MAIL_USERNAME'] = 'friedcomputerz208@gmail.com'
ttt_app.config['MAIL_PASSWORD'] = 'rdjxvuncdfblahtu'
ttt_app.config['MAIL_USE_TLS'] = True
ttt_app.config['MAIL_USE_SSL'] = False

mail = Mail(ttt_app)

ttt_props = {'name': '', 'date' : '', 'grid': [' ', ' ', ' ' , ' ', ' ', ' ', ' ', ' ', ' '], 'winner': ' '}
move_id = 0
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["db"]
users = db['users']
verified_users = db['verified_users']
games = db['games']
keys = db['keys']

def props_clear():
    global ttt_props
    ttt_props = {'name': '', 'date' : '', 'grid': [' ', ' ', ' ' , ' ', ' ', ' ', ' ', ' ', ' '], 'winner': ' '}

def computer_play():
    global ttt_props
    space = randint(0, 8)
    while ttt_props['grid'][space] != ' ':
        space = randint(0, 8)
    ttt_props['grid'][space] = 'O'

def is_winner(player):
    global ttt_props
    # Columns
    if ttt_props['grid'][0] == ttt_props['grid'][3] == ttt_props['grid'][6] == player: # or ttt_props['grid'][0] == \ttt_props['grid'][3] == ttt_props['grid'][6] == 'O':
        return True
    elif ttt_props['grid'][1] == ttt_props['grid'][4] == ttt_props['grid'][7] == player:
        return True
    elif ttt_props['grid'][2] == ttt_props['grid'][5] == ttt_props['grid'][8] == player:
        return True
    # Rows
    elif ttt_props['grid'][0] == ttt_props['grid'][1] == ttt_props['grid'][2] == player:
        return True
    elif ttt_props['grid'][3] == ttt_props['grid'][4] == ttt_props['grid'][5] == player:
        return True
    elif ttt_props['grid'][6] == ttt_props['grid'][7] == ttt_props['grid'][8] == player:
        return True
    # Diagonals
    elif ttt_props['grid'][0] == ttt_props['grid'][4] == ttt_props['grid'][8] == player:
        return True
    elif ttt_props['grid'][2] == ttt_props['grid'][4] == ttt_props['grid'][6] == player:
        return True

# Default route, login
@ttt_app.route('/login', methods=['GET', 'POST'])
def login():
    print("Login")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # First check that user is a verified user
        if users.find_one({"username": username}):
            user_info = users.find_one({"username": username})
            if not verified_users.find_one({"username": username}):
                flash('User Not Verified Yet')
                print('User Not Verified Yet')
                return render_template('hw1login.html')
            elif (user_info['password'] == password):
                flash('Login Successful - Redirecting to Game')
                print('Login Successful - Redirecting to Game')
                return jsonify({"status":"OK"})
                #return redirect('/ttt/play')
            else:
                flash('Login Error')
                print('Login Error')
                return jsonify({"status": "ERROR"})
                #return render_template('hw1login.html')
        else:
            flash('User Not Registered')
            print('User Not Registered')
            return render_template('hw1login.html')
    else:
        print("GET request")
        return render_template('hw1login.html')

# Add user
@ttt_app.route('/', methods=['GET', 'POST'])
@ttt_app.route('/ttt', methods=['GET', 'POST'])
@ttt_app.route('/ttt/', methods=['GET', 'POST'])
@ttt_app.route('/adduser', methods=['GET', 'POST'])
def index():
    print("Add user")
    global move_id
    move_id += 1
    global ttt_props
    print("Finding request method")
    if request.method == 'POST':
        print("POST request")
        # Gather the details and add to users DB
        request.form = request.form.to_dict()
        if not request.form.has_key('name'):
            print("Bad form formatting")
            return jsonify({"status":"OK"})
        print(request.form)
        name = request.form['name']
        print("Obtained name")
        ttt_props['name'] = name
        print("Now let's get the email")
        mail_addr = request.form['email']
        print(name + " " + mail_addr)
        userinfo = {'username': name, 'password': request.form['password'], 'email': mail_addr}
        print(userinfo)
        users.insert_one(userinfo)
        print("Inserted user into users collection")

        # Send the message
        msg = Message("Tic-Tac-Toe Registration", sender="dsli@tictactoe.com")
        key = "abracadabra"  # temporary string until we can generate something random
        msg.body = "The key is: " + key
        msg.add_recipient(mail_addr)
        mail.send(msg)

        # Get the email-key pair and add it to the keys DB
        keypair = {'email': mail_addr, 'key': key}
        keys.insert_one(keypair)
        print("Inserted key into keys collection")

        # return redirect
        print("Redirecting to verify page")
        return jsonify({"status":"OK"})
        #return redirect("/verify", code=302)
    else:
        print("Add user GET request")
        props_clear()
        ttt_grid = json.dumps(ttt_props)
        return render_template('hw1.html', name=None, winner=None, email=None, board=ttt_grid, getupdate=False, id=move_id)

# Verify user, send message with key
@ttt_app.route('/verify', methods=['GET', 'POST'])
def send_verification():
    if request.method == 'POST':
        print("Post request, verifying")
        email_addr = request.form['email']
        key = request.form['key']

        # Get email-key pairing from database

        email_key_pair = keys.find_one({'email': email_addr})
        print(email_key_pair)
        user_info = users.find_one({'email': email_addr})
        print(user_info)
        if key == email_key_pair['key']:
            verified_users.insert_one({"username": user_info['username'], "email": email_addr})
            print("verified")
            return jsonify({"status":"OK"})
            # return redirect("/login", code=302)
        else:
            flash("Problem")
            return jsonify({"status": "ERROR"})
            #return render_template('hw1verify.html')
    else:
        print("Verify GET request")
        return render_template('hw1verify.html')


@ttt_app.route('/ttt/play/', methods=['POST', 'GET'])
@ttt_app.route('/ttt/play', methods=['POST', 'GET'])
def board():
    global move_id
    global ttt_props
    move_id += 1

    if request.method == 'POST':
        print("request grid")
        print(request.json['grid'])
        ttt_props['grid'] = request.json['grid']
        if is_winner('X') and ttt_props['winner'] == ' ':
            ttt_props['winner'] = 'X'
            ttt_grid = json.dumps(ttt_props)
            print(ttt_props)
            jify = jsonify(ttt_props)
            print(jify)
            return jify
        else:
            computer_play()
            if is_winner('O') and ttt_props['winner'] == ' ':
                ttt_props['winner'] = 'O'
    #            ttt_grid = json.dumps(ttt_props)
                print(ttt_props)
                jify = jsonify(ttt_props)
                print(jify)
                return jify
            else:
                ttt_grid = json.dumps(ttt_props)
                print(ttt_props)
                jify = jsonify(ttt_props)
                print(jify)
                return jify
    else:
        ttt_grid = json.dumps(ttt_props)
        jify = jsonify(ttt_props)
        return jify

if __name__ == '__main__':
    ttt_app.run(debug=True)
    # ttt_app.run(debug = True, host='0.0.0.0', port=80)
