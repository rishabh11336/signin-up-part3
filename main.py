from flask import Flask, render_template, session, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "database.sqlite3") 
db = SQLAlchemy()
db.init_app(app)

#session
app.secret_key = os.urandom(24)

from model import *
db.init_app(app)
app.app_context().push()

@app.route('/')
def Hello_world():
    if 'user_id' in session:
        return render_template('index.html')
    else:
        return redirect('/sign-in')

@app.route('/sign-in')
def sign_in():
    return render_template('sign-in.html')

@app.route('/sign-up')
def sign_up():
    return render_template('sign-up.html')

@app.route('/login-action', methods=['POST'])
def login_action():
    email = request.form.get('email')
    password = request.form.get('password')

    users = User.query.filter_by(email=email, password=password)
    check = [ user for user in users]
    if check:
        session['user_id'] = check[0].id
        return redirect('/')
    else:
        return redirect('/sign-in')

@app.route('/register', methods=['POST'])
def register():
    try:
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        contact = request.form.get('contact')
        update_user = User(email=email, name=name, password=password, contact=contact)
        db.session.add(update_user)
        db.session.flush()
    except Exception as e:
        return "{}".format(e),"not registered"
    else:
        db.session.commit()
        users = User.query.filter_by(email=email, password=password)
        check = [ user for user in users]
        if check:
            session['user_id'] = check[0].id
            return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('sign-in')




if __name__ == '__main__':
    app.run(debug=True)