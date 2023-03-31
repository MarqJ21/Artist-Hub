from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import pprint

db = "artist_schema"
class Song:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.genre = data['genre']
        self.feature = data['feature']
        self.bpm = data['bpm']
        self.link = data['link']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO song (title, genre, feature, bpm, link, user_id) VALUES (%(title)s, %(genre)s, %(feature)s, %(bpm)s, %(link)s, %(user_id)s);"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM song"
        results = connectToMySQL(db).query_db(query)
        all_songs  = []
        for shows in results:
            all_songs.append(cls(shows))
        return all_songs

    @classmethod
    def get_song_by_id(cls,data):
        query = "SELECT * FROM song WHERE id = %(id)s"
        results = connectToMySQL(db).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def update_song(cls, data):
        query = "UPDATE song set title = %(title)s, genre = %(genre)s, feature = %(feature)s, bpm = %(bpm)s, link = %(link)s WHERE id = %(id)s"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def validate_song(cls, Song):
        is_valid = True
        if len(Song['title']) < 2:
            flash("Title must be at least 3 characters")
            is_valid = False
        if len(Song['genre']) < 2:
            flash("Genre must be at least 3 characters")
            is_valid = False
        return is_valid

    @classmethod
    def delete_song(cls,id):
        query = f"DELETE FROM song WHERE id = {id}"
        return connectToMySQL(db).query_db(query)
    

