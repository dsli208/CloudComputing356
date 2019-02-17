from flask import Flask, Blueprint, render_template, request, url_for
import time
# from app.ttt_bp import ttt_bp

ttt_app = Flask(__name__)

# ttt_app.register_blueprint(ttt_bp, url_prefix='/ttt')

@ttt_app.route('/ttt', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
        return render_template('hw1.html', name=name, date=date)
    else:
        return render_template('hw1.html')

if __name__ == '__main__':
   ttt_app.run(debug = True)
