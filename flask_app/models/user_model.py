from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.song_model import Song
from flask import flash
import re
import pprint

db = "artist_schema"

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.username = data['username']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.song = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO user (first_name, last_name, username, email, password) VALUES (%(fname)s, %(lname)s, %(username)s,%(email)s, %(password)s);"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM user"
        results = connectToMySQL(db).query_db(query)
        all_users  = []
        for user in results:
            all_users.append(cls(user))
        return all_users
    
    @classmethod
    def validate_user(cls, User):
        is_valid = True

        if len(User['fname']) < 2:
            flash("First name must be at least 3 characters")
            is_valid = False
        if len(User['lname']) < 2:
            flash("Last name must be at least 3 characters")
            is_valid = False
        if User['password'] != User['cpass']:
            flash("Passwords don't match")
            is_valid = False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, User['email']):
            flash("Invalid email address")
            is_valid = False
        return is_valid
    
    @classmethod
    def get_single_user(cls, data):
        query = "SELECT * from users where id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM user WHERE email = %(email)s"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False 
        return cls(results[0])
    
    @classmethod
    def get_user_by_id(cls,id):
        query = "SELECT * FROM user WHERE id = %(id)s"
        results = connectToMySQL(db).query_db(query,{'id':id})
        if len(results) < 1:
            return False 
        return cls(results[0])
    
    @classmethod 
    def get_single_song(cls,data):
        query = "SELECT * FROM user left join song ON song.user_id = user.id where song.id = %(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        user = cls(results[0])
        for song in results:
            song_dictionary ={
                'id' : song["song.id"],
                'title' : song['title'],
                'feature': song['feature'],
                'genre' : song['genre'],
                'bpm' : song['bpm'],
                'link' : song['link'],
                'created_at' : song['song.created_at'],
                'updated_at' : song['song.updated_at']
            }
            user.song.append(Song(song_dictionary)) 
        return user