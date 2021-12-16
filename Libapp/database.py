from flask_login import UserMixin
from __init__ import db

class User(UserMixin ,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False )
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username , password , email):
        self.username = username
        self.password = password 
        self.email = email 




