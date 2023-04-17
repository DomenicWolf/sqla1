"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func

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
    
class Post(db.Model):
    """Post model"""
    __tablename__ = 'posts'

    def __repr__(self):
        p = self
        return f'id = {self.id} title = {self.title}'
    
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    
    title = db.Column(db.String,
                      nullable=False)
    
    content = db.Column(db.String,
                        nullable=False)
    
    created_at = db.Column(db.DateTime, 
                           default=func.now())
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    userss = db.relationship('User',backref = 'posts')

    tags = db.relationship('Tag',secondary='post_tags',backref = 'posts')

class Tag(db.Model):
    """tag model"""

    __tablename__ = 'tags'

    def __repr__(self):
        return f"{self.name}"
    
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    
    name = db.Column(db.Text,
                     unique = True)
    

class PostTag(db.Model):
    """tag model"""

    __tablename__ = 'post_tags'

    def __repr__(self):
        return f'{self.post_id} {self.tag_id}'
    
    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key = True)
    

    
    
