from random import randint
from flask import Flask, render_template, request, url_for, jsonify
import time
from flask_restful import Api, Resource, reqparse
# from app.ttt_bp import ttt_bp

ttt_app = Flask(__name__)
username = ""
date = ""
ttt_props = {"grid": [' ', ' ', ' ' , ' ', ' ', ' ', ' ', ' ', ' '], "winner": ' '}

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
@ttt_app.route('/', methods=['POST', 'GET'])
@ttt_app.route('/ttt', methods=['POST', 'GET'])
@ttt_app.route('/ttt/', methods=['POST', 'GET'])
def index():
    date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
    if request.method == 'POST':
        name = request.form['Name']
        username = name
        return render_template('hw1.html', name=name, date=date, winner=None, grid=ttt_props)
    else:
        return render_template('hw1.html', name=None, date=None, winner=None, grid=ttt_props)

@ttt_app.route('/ttt/play', methods=['POST', 'GET'])
@ttt_app.route('/ttt/play/', methods=['POST', 'GET'])
def board(player, space):
    if request.method == 'POST':
        if ttt_props['grid'][space] == ' ':
            ttt_props['grid'][space] = player
            if is_winner(player):
                ttt_props['winner'] = player
                return render_template('hw1.html', name=username, date=date, winner=player, grid=ttt_props)
            else:
                computer_play()
                if is_winner('O'):
                    ttt_props['winner'] = 'O'
                    return render_template('hw1.html', name=username, date=date, winner='O', grid=ttt_props)
                else:
                    return render_template('hw1.html', name=username, date=date, winner=None, grid=ttt_props)
        else:
            pass

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