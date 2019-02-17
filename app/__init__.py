from flask import Flask, Blueprint, render_template
# from app.ttt_bp import ttt_bp

ttt_app = Flask(__name__)

# ttt_app.register_blueprint(ttt_bp, url_prefix='/ttt')

@ttt_app.route('/ttt', methods=['POST', 'GET'])
def index():
   return render_template('hw1.html')

if __name__ == '__main__':
   ttt_app.run(debug = True)
