"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Users table"""
    __tablename__ = "users"

    def __repr__(self):
        p = self
        return f"Name = {p.first_name} {p.last_name}"

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    first_name = db.Column(db.String,
                           nullable = False)
    last_name = db.Column(db.String,
                          nullable = False)
    image_url = db.Column(db.String,
                          default = 'https://as1.ftcdn.net/v2/jpg/01/90/92/08/1000_F_190920807_lUTBNhoGY9blKO1eblfq8s2GpVbKhEUI.jpg')
    
