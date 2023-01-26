from main import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key = True)
    email = db.Column(db.String(100))
    password = db.Column(db.String)
    contact = db.Column(db.Integer)
    name = db.Column(db.String(50))