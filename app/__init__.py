from flask import Flask, render_template, request, url_for, jsonify
import time
from flask_restful import Api, Resource, reqparse
# from app.ttt_bp import ttt_bp

ttt_app = Flask(__name__)

ttt_props = {"grid": [' ', ' ', ' ' , ' ', ' ', ' ', ' ', ' ', ' '], "winner": ' '}

# ttt_app.register_blueprint(ttt_bp, url_prefix='/ttt')

@ttt_app.route('/ttt', methods=['POST', 'GET'])
def index():
    date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
    if request.method == 'POST':
        name = request.form['Name']

        return render_template('hw1.html', name=name, date=date)
    else:
        return render_template('hw1.html', name=None, date=date)

@ttt_app.route('/ttt/play', methods=['POST', 'GET'])
def get_board():
    return jsonify(ttt_props)

class Game(Resource):
    def get(self, name):
        pass

    def post(self, name):
        pass

    def put(self, name):
        pass

    def delete(self, name):
        pass

if __name__ == '__main__':
    ttt_app.run(debug=True)
    #ttt_app.run(debug = True, host='0.0.0.0', port=80)
