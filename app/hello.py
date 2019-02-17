from flask import Flask, redirect, url_for, request, render_template
import time
app = Flask(__name__)

#@app.route('/')
#def success(name):
#    return "Hello " + name + "," + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())

@app.route('/', methods = ['POST'], url_prefix='/ttt')
def login():
   if request.method == 'POST':
      name = request.form['name']
      date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
      #return redirect(url_for('success',name=name))
      return render_template('app/templates/hw1.html', name=name, date=date)
   else:
      return render_template('app/templates/hw1.html')

if __name__ == '__main__':
   app.run(debug = True)