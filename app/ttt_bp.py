from flask import Blueprint, render_template, request
import time

ttt_bp = Blueprint("ttt", __name__)

@ttt_bp.route("/", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        # date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
        # return redirect(url_for('success',name=name))
        return render_template('hw1.html', name=name)
    else:
        return render_template('hw1.html')

@ttt_bp.route('/play')
def play_ttt():
    pass
