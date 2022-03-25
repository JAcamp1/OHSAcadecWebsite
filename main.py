from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy, Model
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
import pandas as pd

app = Flask(__name__)

db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'goes-here'
app.config['SQLALCHEMY_DATABASE_URI']  = 'sqlite:///db.sqlite'

@app.route("/")
def index():
    return render_template('index.html')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first = db.Column(db.String(200))
    last = db.Column(db.String(200))
    roles = db.Column(db.String(200))

@app.route("/competitor")
def competitor():
    return render_template('competitor.html')

@app.route("/admin")
def admin():
    return render_template('admin.html')

@app.route("/admin/registration")
def reg():
    return render_template('registration.html')

@app.route("/admin/registration", methods=['POST'])
def reg_post():
    #registration code
    number = request.form.get('num')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    password = request.form.get('password')
    conpassword = request.form.get('conpassword')

    if password == conpassword:
        user = User.query.filter_by(number=number).first()
        if user is None:
            new_user = User(number=number, password=generate_password_hash(password, method='sha256'), first=firstname, last=lastname)
            db.session.add(new_user)
            db.session.commit()
            print("New user registered under the number " + new_user.number + " and the name " + new_user.first + " " + new_user.last + ".")
            flash('user registered! Name: ' + firstname)
            return redirect(url_for('admin'))
        else:
            flash('User already exists!')
            print("User create attempt failed: user already exists.")
            return redirect(url_for('admin'))
    else:
        flash('Passwords do not match!')
        print("Password check failed.")
        return redirect(url_for('admin'))


@app.route('/login', methods=['POST'])
#defines login page
def login():
    return render_template('login.html')
#verifies against db
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials

app.run()