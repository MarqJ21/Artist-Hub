from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user_model import User
from flask_app.models.song_model import Song


@app.route('/create_song')
def index_tsong():
    return render_template("create_song.html")

@app.route("/add_song", methods=[ "post"])
def create_song():
    
    data = {
        "title": request.form['title'],
        "genre": request.form['genre'],
        "feature": request.form['feature'],
        "bpm": request.form['bpm'],
        "link": request.form['link'],
        "user_id": session['user_id']
    }

    if not Song.validate_song(data):
        return redirect("/create_song")
    
    Song.save(data)
    return redirect ("/display_songs")

@app.route("/show/<int:id>")
def show_one_song(id):
    data = {
        'id' : id
    }
    return render_template("show_song.html", one_user = User.get_single_song(data))

@app.route("/edit/<int:id>")
def edit_one_song(id):
    data = {
        'id' : id
    }
    return render_template("edit_song.html", one_user = Song.get_song_by_id(data))

@app.route("/update_song", methods=[ "post"])
def update_song():
    
    data = {
        "title": request.form['title'],
        "genre": request.form['genre'],
        "feature": request.form['feature'],
        "bpm": request.form['bpm'],
        "link": request.form['link'],
        "id": request.form['id']
    }

    if not Song.validate_song(data):
        return redirect("/display_songs")
    
    Song.update_song(data)
    return redirect("/display_songs")

@app.route("/delete/<int:id>")
def delete_song(id):
    Song.delete_song(id)
    return redirect("/display_songs")