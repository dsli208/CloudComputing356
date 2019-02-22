from random import randint
import json

from flask import Flask, render_template, request, url_for, jsonify
import time

ttt_app = Flask(__name__)
ttt_props = {'name': '', 'date' : '', 'grid': [' ', ' ', ' ' , ' ', ' ', ' ', ' ', ' ', ' '], 'winner': ' '}
move_id = 0

def props_clear():
    global ttt_props
    ttt_props = {'name': '', 'date' : '', 'grid': [' ', ' ', ' ' , ' ', ' ', ' ', ' ', ' ', ' '], 'winner': ' '}
    # print(ttt_props)
    # print("Props cleared")

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

# ttt_app.register_blueprint(ttt_bp, url_prefix='/ttt')
@ttt_app.route('/', methods=['GET', 'POST'])
@ttt_app.route('/ttt/', methods=['GET', 'POST'])
@ttt_app.route('/ttt', methods=['GET', 'POST'])
def index():
    global move_id
    move_id += 1
    global ttt_props
    date = time.strftime("%Y-%m-%d", time.gmtime())
    if request.method == 'POST':
        # print('POST request')
        name = request.form['name']
        ttt_props['name'] = name
        ttt_props['date'] = date
        ttt_grid = json.dumps(ttt_props)
        return render_template('hw1.html', name=ttt_props['name'], date=date, winner=None, board=ttt_grid, getupdate=False, id=move_id)
    else:
        props_clear()
        # print('GET request')
        ttt_grid = json.dumps(ttt_props)
        # print(ttt_props)
        return render_template('hw1.html', name=None, date=None, winner=None, board=ttt_grid, getupdate=False, id=move_id)

@ttt_app.route('/ttt/play/', methods=['POST', 'GET'])
@ttt_app.route('/ttt/play', methods=['POST', 'GET'])
def board():
    global move_id
    global ttt_props
    move_id += 1
    # print('Request JSON')

    if request.method == 'POST':
        # print(request.json)
        space = int(request.json['grid_id'])
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
    # return render_template('hw1.html', name=ttt_props['name'], date=ttt_props['date'], winner='O', board=ttt_grid, getupdate=True, id=move_id)
    #        else:
    #            ttt_grid = json.dumps(ttt_props)
    # print(ttt_props)
    #            jify = jsonify(ttt_props)
    # print(jify)
    #            return jify
        # if ttt_props['grid'][space] == ' ':
        #    ttt_props['grid'][space] = 'X'
        #    if is_winner('X'):
        #        ttt_props['winner'] = 'X'
        #        ttt_grid = json.dumps(ttt_props)
                # print(ttt_props)
        #        jify = jsonify(ttt_props)
                # print(jify)
        #        return jify
                #return render_template('hw1.html', name=ttt_props['name'], date=ttt_props['date'], winner='X', board=ttt_grid, getupdate=True, id=move_id)
        #    else:
        #        computer_play()
        #        if is_winner('O'):
        #            ttt_props['winner'] = 'O'
        #            ttt_grid = json.dumps(ttt_props)
                    # print(ttt_props)
        #            jify = jsonify(ttt_props)
                    # print(jify)
        #            return jify
                    # return render_template('hw1.html', name=ttt_props['name'], date=ttt_props['date'], winner='O', board=ttt_grid, getupdate=True, id=move_id)
        #        else:
        #            ttt_grid = json.dumps(ttt_props)
                    # print(ttt_props)
        #            jify = jsonify(ttt_props)
                    # print(jify)
        #            return jify
                    # return render_template('hw1.html', name=ttt_props['name'], date=ttt_props['date'], winner=None, board=ttt_grid, getupdate=True, id=move_id)
        #else:
        #    ttt_grid = json.dumps(ttt_props)
            # print(ttt_grid)
        #    jify = jsonify(ttt_props)
            # print(jify)
        #    return jify
            # return render_template('hw1.html', name=ttt_props['name'], date=ttt_props['date'], winner=None, board=ttt_grid, getupdate=False, id=move_id)
    else:
        ttt_grid = json.dumps(ttt_props)
        # print(ttt_props)
        jify = jsonify(ttt_props)
        # print(jify)
        return jify
        # return render_template('hw1.html', name=ttt_props['name'], date=ttt_props['date'], winner=None, board=ttt_grid, getupdate=False, id=move_id)

if __name__ == '__main__':
    ttt_app.run(debug=True)
    #ttt_app.run(debug = True, host='0.0.0.0', port=80)
