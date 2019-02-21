from random import randint
import json

from flask import Flask, render_template, request, url_for, jsonify
import time
from flask_restful import Api, Resource, reqparse

ttt_app = Flask(__name__)
ttt_props = {"name": "", "date": "", "grid": [' ', ' ', ' ' , ' ', ' ', ' ', ' ', ' ', ' '], "winner": ' '}

def props_clear():
    global ttt_props
    ttt_props = {"grid": [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], "winner": ' '}
    print(ttt_props)

def computer_play():
    space = randint(0, 8)
    while ttt_props['grid'][space] != ' ':
        space = randint(0, 8)
    ttt_props['grid'][space] = 'O'

def is_winner(player):
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

# ttt_app.register_blueprint(ttt_bp, url_prefix='/ttt')
@ttt_app.route('/', methods=['GET'])
@ttt_app.route('/ttt/', methods=['GET', 'POST'])
@ttt_app.route('/ttt', methods=['GET', 'POST'])
def index():
    date = time.strftime("%Y-%m-%d", time.gmtime())
    if request.method == 'POST':
        print('POST request')
        name = request.form['name']
        ttt_props['name'] = name
        ttt_props['date'] = date
        ttt_grid = json.dumps(ttt_props)
        return render_template('hw1.html', name=ttt_props['name'], date=date, winner=None, board=ttt_grid)
    else:
        props_clear()
        print('GET request')
        ttt_grid = json.dumps(ttt_props)
        print(ttt_props)
        return render_template('hw1.html', name=None, date=None, winner=None, board=ttt_grid)

@ttt_app.route('/ttt/play', methods=['POST', 'GET'])
@ttt_app.route('/ttt/play/', methods=['POST', 'GET'])
def board():
    print(request.json)
    space = int(request.json['grid_id'])
    if request.method == 'POST':
        if ttt_props['grid'][space] == ' ':
            ttt_props['grid'][space] = 'X'
            if is_winner('X'):
                ttt_props['winner'] = 'X'
                ttt_grid = json.dumps(ttt_props)
                print(ttt_props)
                return render_template('hw1.html', name=ttt_props['name'], date=ttt_props['date'], winner='X', grid=ttt_grid)
            else:
                computer_play()
                if is_winner('O'):
                    ttt_props['winner'] = 'O'
                    ttt_grid = json.dumps(ttt_props)
                    print(ttt_props)
                    return render_template('hw1.html', name=ttt_props['name'], date=ttt_props['date'], winner='O', grid=ttt_grid)
                else:
                    ttt_grid = json.dumps(ttt_props)
                    print(ttt_props)
                    return render_template('hw1.html', name=ttt_props['name'], date=ttt_props['date'], winner=None, grid=ttt_grid)
        else:
            ttt_grid = json.dumps(ttt_props)
            print(ttt_grid)
            return render_template('hw1.html', name=ttt_props['name'], date=ttt_props['date'], winner=None, grid=ttt_grid)

if __name__ == '__main__':
    ttt_app.run(debug=True)
    #ttt_app.run(debug = True, host='0.0.0.0', port=80)


#class Game(Resource):
#    def is_winner(self):
        # Columns
#        if ttt_props['grid'][0] == ttt_props['grid'][3] == ttt_props['grid'][6] == 'X' or ttt_props['grid'][0] == ttt_props['grid'][3] == ttt_props['grid'][6] == 'O':
#            return True
#        elif ttt_props['grid'][1] == ttt_props['grid'][4] == ttt_props['grid'][7] == 'X' or ttt_props['grid'][1] == ttt_props['grid'][4] == ttt_props['grid'][7] == 'O':
#            return True
#        elif ttt_props['grid'][2] == ttt_props['grid'][5] == ttt_props['grid'][8] == 'X' or ttt_props['grid'][2] == ttt_props['grid'][5] == ttt_props['grid'][8] == 'O':
#            return True
        # Rows
#        elif ttt_props['grid'][0] == ttt_props['grid'][1] == ttt_props['grid'][2] == 'X' or ttt_props['grid'][0] == ttt_props['grid'][1] == ttt_props['grid'][2] == 'O':
#            return True
#        elif ttt_props['grid'][3] == ttt_props['grid'][4] == ttt_props['grid'][5] == 'X' or ttt_props['grid'][3] == ttt_props['grid'][4] == ttt_props['grid'][5] == 'O':
#            return True
#        elif ttt_props['grid'][6] == ttt_props['grid'][7] == ttt_props['grid'][8] == 'X' or ttt_props['grid'][6] == ttt_props['grid'][7] == ttt_props['grid'][8] == 'O':
#            return True
        # Diagonals
#        elif ttt_props['grid'][0] == ttt_props['grid'][4] == ttt_props['grid'][8] == 'X' or ttt_props['grid'][0] == ttt_props['grid'][4] == ttt_props['grid'][8] == 'O':
#            return True
#        elif ttt_props['grid'][2] == ttt_props['grid'][4] == ttt_props['grid'][6] == 'X' or ttt_props['grid'][2] == ttt_props['grid'][4] == ttt_props['grid'][6] == 'O':
#            return True

#    def get(self, player, space):
#        return jsonify(ttt_props)

#    def post(self, player, space):
#        if ttt_props['grid'][space] == ' ':
#            ttt_props['grid'][space] = player
#        else:
#            pass

 #   def put(self, name):
 #       pass

 #   def delete(self, name):
 #       pass