import pymongo
from random import randint
import json
import time

from flask import Flask, render_template, request, url_for, jsonify, redirect, flash, session
from flask_mail import Mail, Message
from flask_pymongo import PyMongo
from flask_session import Session

ttt_app = Flask(__name__)

# Mail Server Config
ttt_app.config['MAIL_SERVER']='smtp.gmail.com'
ttt_app.config['MAIL_PORT'] = 587
ttt_app.config['MAIL_USERNAME'] = 'friedcomputerz208@gmail.com'
ttt_app.config['MAIL_PASSWORD'] = 'rdjxvuncdfblahtu'
ttt_app.config['MAIL_USE_TLS'] = True
ttt_app.config['MAIL_USE_SSL'] = False

mail = Mail(ttt_app)

# Flask Session Config
ttt_app.config['SESSION_TYPE'] = 'mongodb'

Session(ttt_app)

ttt_props = {'status':' ', 'grid': [' ', ' ', ' ' , ' ', ' ', ' ', ' ', ' ', ' '], 'winner': ' '}
move_id = 0
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["db"]
users = db['users']
verified_users = db['verified_users']
games = db['games'] # Stores in nested dictionaries by user and next game id : dictionary of past games
keys = db['keys']

def props_clear():
    global ttt_props
    ttt_props = {'status':'OK', 'grid': [' ', ' ', ' ' , ' ', ' ', ' ', ' ', ' ', ' '], 'winner': ' '}

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

# List Games
# When getting games, get those ONLY where the USERNAME MATCHES
@ttt_app.route('/listgames', methods=['GET', 'POST'])
def list_games():
    if 'username' in session:
        username = session['username']
        print(username + ' is currently logged in')
        user_data = games.find_one({'username':username})
        if user_data is None:
            print(username + "'s data was somehow not found")
            return jsonify({"status": "OK", "games": []})
        else:
            print(user_data)
            return jsonify({"status": "OK", "games":user_data['game_list']})
    else:
        return jsonify({"status":"OK", "games":[]})

@ttt_app.route('/getgame', methods=["GET", "POST"])
def get_game():
    if 'username' not in session:
        print("Nobody Logged In")
        return jsonify({"status": "ERROR"})

    username = session['username']
    form = request.json
    print(form)
    if not 'id' in form:
        print("Bad Formatting")
        return jsonify({"status":"ERROR"})

    id = form['id']
    user = games.find_one({"username":username})
    user_games = user['game_list']

    for g in user_games:
        if g['id'] == id:
            return jsonify({"status":"OK", "grid": g['props']['grid'], "winner":g['props']['winner']}) #, "grid": g['props']['grid'], "winner":g['props']['winner']

    return jsonify({"status":"ERROR"})

@ttt_app.route('/getscore', methods=['GET', 'POST'])
def get_score():
    if 'username' not in session:
        print("Nobody Logged In")
        return jsonify({"status": "ERROR"})

    username = session['username']
    user = games.find_one({"username": username})
    user_games = user['game_list']

    x_win = 0
    o_win = 0
    ties = 0
    for g in user_games:
        if g['props']['winner'] == 'X':
            x_win += 1
        elif g['props']['winner'] == 'O':
            o_win += 1

    return jsonify({"status":"OK", "human":x_win, "wopr":o_win, "tie":ties})

# Logout
@ttt_app.route('/logout', methods=['GET', 'POST'])
def logout():
    print("Logging out")
    session.pop('username', None)
    return jsonify({"status": "OK"})

# Default route, login
@ttt_app.route('/login', methods=['GET', 'POST'])
def login():
    print("Login")
    if request.method == 'POST':
        # Verify request form
        form = request.json
        print(request.json)

        if not 'username' in form or not 'password' in form:
            print("Bad form formatting")
            return jsonify({"status": "OK"})

        username = form['username']
        password = form['password']

        # First check that user is a verified user
        if users.find_one({"username": username}):
            user_info = users.find_one({"username": username})
            if not verified_users.find_one({"username": username}):
                # flash('User Not Verified Yet')
                print('User Not Verified Yet')
                return jsonify({"status": "ERROR"})
            elif (user_info['password'] == password):
                # flash('Login Successful - Redirecting to Game')
                print('Login Successful - Redirecting to Game')

                # Login success - store username in session
                if 'username' not in session:
                    session['username'] = username

                return jsonify({"status":"OK"})
                #return redirect('/ttt/play')
            else:
                # flash('Login Error')
                print('Login Error')
                return jsonify({"status": "ERROR"})
                #return render_template('hw1login.html')
        else:
            # flash('User Not Registered')
            print('User Not Registered')
            return jsonify({"status": "ERROR"})
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
        form = request.json
        print(request.json)

        if not 'username' in form:
            print("Bad form formatting")
            return jsonify({"status":"OK"})

        name = form['username']
        print("Obtained name")
        ttt_props['name'] = name
        print("Now let's get the email")
        mail_addr = form['email']
        print(name + " " + mail_addr)
        userinfo = {'username': name, 'password': form['password'], 'email': mail_addr}
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
        redirect('/verify', code=200)
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

        # Verify request form
        form = request.json
        print(request.json)

        if not 'email' in form or not 'key' in form:
            print("Bad form formatting")
            return jsonify({"status": "OK"})

        email_addr = form['email']
        key = form['key']

        # Get email-key pairing from database

        email_key_pair = keys.find_one({'email': email_addr})
        print(email_key_pair)
        user_info = users.find_one({'email': email_addr})
        print(user_info)
        if key == email_key_pair['key']:
            # Add user to verified users DB
            verified_users.insert_one({"username": user_info['username'], "email": email_addr})
            print("verified")

            # Now, create their game properties
            user_games_list = []
            user_game_data = {'username':user_info['username'],'id': 100, "game_list":user_games_list}
            games.insert_one(user_game_data)

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
        if not 'username' in session:
            return jsonify({"status": "ERROR"})
        print("request grid")
        print(request.json)

        # Handle NoneType move case
        if request.json['move'] is None:
            print("NoneType move detected")
            ttt_props['winner'] = ' '
            ttt_props['status'] = 'OK'
            print(ttt_props)
            return jsonify(ttt_props)

        if ttt_props['grid'][request.json['move']] != ' ':
            print("Space is already taken")
            jify = jsonify(ttt_props)
            print(jify)
            return jify

        ttt_props['grid'][request.json['move']] = 'X'
        # ttt_props['grid'] = request.json['grid']
        if is_winner('X') and ttt_props['winner'] == ' ':
            print("X wins")
            # Mark X as the winner and prepare the winner file (ttt_props)
            ttt_props['winner'] = 'X'
            ttt_grid = json.dumps(ttt_props)
            ttt_props['status'] = 'OK'
            print(ttt_props)
            jify = jsonify(ttt_props)

            # Store the game in the user's games list array in the DB
            # First get the array
            username = session['username']
            game_info_db = games.find_one({"username": username})
            start_date = time.strftime("%Y-%m-%d", time.gmtime())
            saved_game_data = {"id":game_info_db['id'], "start_date": start_date, "props": ttt_props} # put props key in here?
            # Append game data to past games array
            game_info_db['game_list'].append(saved_game_data)
            # Update ID
            new_id = game_info_db['id'] + 1

            # Update the games DB
            games.update_one({"username":username}, {'$set': {'id': new_id, 'game_list': game_info_db['game_list']}}, upsert=False)

            # Reset board
            props_clear()

            print(jify)
            return jify
        else:
            computer_play()
            if is_winner('O') and ttt_props['winner'] == ' ':
                print("Computer wins")
                ttt_props['winner'] = 'O'
    #            ttt_grid = json.dumps(ttt_props)
                print(ttt_props)
                jify = jsonify(ttt_props)

                # Store the game in the user's games list array in the DB
                # First get the array
                username = session['username']
                game_info_db = games.find_one({"username": username})
                start_date = time.strftime("%Y-%m-%d", time.gmtime())
                saved_game_data = {"id": game_info_db['id'], "start_date": start_date} # put props key in here?
                # Append game data to past games array
                game_info_db['game_list'].append(saved_game_data)
                # Update ID
                new_id = game_info_db['id'] + 1

                # Update the games DB
                games.update_one({"username": username}, {'$set': {'id': new_id, 'game_list': game_info_db['game_list']}}, upsert=False)

                # Reset board
                props_clear()

                print(jify)
                return jify
            else:
                print("On to the next set of turns")
                ttt_grid = json.dumps(ttt_props)
                print(ttt_props)
                jify = jsonify(ttt_props)
                print(jify)
                return jify
    else:
        print("/ttt/play GET request")
        ttt_grid = json.dumps(ttt_props)
        jify = jsonify(ttt_props)
        return jify

if __name__ == '__main__':
    ttt_app.run(debug=True)
    # ttt_app.run(debug = True, host='0.0.0.0', port=80)
