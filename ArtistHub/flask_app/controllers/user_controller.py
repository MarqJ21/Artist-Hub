from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user_model import User
from flask_app.models.song_model import Song
import pprint
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/display_songs")
def success():
    if 'user_id' not in session:
        flash("You need to log in before accessing this page")
        return redirect('/')
    users = User.get_all()
    songs = Song.get_all()
    
    return render_template("songs.html", all_users = users, user = User.get_user_by_id(session['user_id']), all_songs = songs)

@app.route("/create_user", methods=[ "post"])
def create_user():
    if  User.get_by_email(request.form) == True:
        flash("email is already in use or password and confrim password do not match")
        return redirect('/')
    
    data = {
        'fname' :request.form['fname'],
        'lname' :request.form['lname'],
        'username' :request.form['username'],
        'email' :request.form['email'],
        'password' :request.form['password'],
        'cpass' :request.form['cpass']
    }

    if not User.validate_user(data):
        return redirect('/')
    
    data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    del data['cpass']

    user_id = User.save(data)
    print(data)
    session['user_id'] = user_id
    return redirect("/")

@app.route("/login", methods =['post'])
def login():
    data = {
        'email' :request.form['email']
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('Email or password not correct')
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Email or password not correct')
        return redirect("/")
    session['user_id'] = user_in_db.id
    return redirect("/display_songs")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
