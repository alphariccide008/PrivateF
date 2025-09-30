from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer)
    level = db.Column(db.String(20))
    school = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    guardian = db.Column(db.String(120))
    occupation = db.Column(db.String(120))
    status = db.Column(db.String(120))
    approved = db.Column(db.String(120))

    # one-to-one relationship
    info = db.relationship("Information", backref="user", uselist=False)

     


class Information(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    financial = db.Column(db.Text)
    intelligence = db.Column(db.Text)
    grit = db.Column(db.Text)
    growth = db.Column(db.Text)
    giving_back = db.Column(db.Text)

    waec_file = db.Column(db.String(255))
    jamb_file = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)





class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(300), nullable=False)