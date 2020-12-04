from flask import Flask,render_template,request,url_for,redirect,flash
app = Flask(__name__)
app.secret_key='secret'

@app.route('/')

def login():
    return render_template('login.html')

@app.route('/register')

def register():
    return render_template('register.html')


if __name__=="__main__":
    app.run(host="localhost",port="8888")