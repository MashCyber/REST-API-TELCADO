import sqlite3
from db import db

class UserModel(db.Model): #extends the Model class for db
    #the tables to be accessed
    __tablename__ = 'users'
    # alchemy creates table and maps below columns 
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    
    def __init__(self,username,password):
        self.username = username
        self.password = password
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def find_by_username(cls,username):
        user = UserModel.query.filter_by(username=username).first() #SELECT * FROM users WHERE username=username LIMIT 1
        return user
    
    @classmethod
    def find_by_id(cls,_id):
        user = UserModel.query.filter_by(id=_id).first() #SELECT * FROM users WHERE id=_id LIMIT 1
        return user
        