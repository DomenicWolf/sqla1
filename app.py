"""Blogly application."""

from flask import Flask,render_template,redirect,request,session,flash
from models import db, connect_db,User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def show_home():
    return redirect('/users')

@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def show_new_user_form():
    return render_template('users/new.html')

@app.route('/users/new', methods=['POST'])
def recieve_form():
    first = request.form['first_name']
    last = request.form['last_name']
    url = request.form['image_url']
    url = url if url else None
    new_user = User(first_name=first,last_name=last,image_url=url)

    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_specific_user(user_id):
    user = User.query.get(user_id)
    return render_template('users/user.html',user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit(user_id):
    user = User.query.get(user_id)
    return render_template('users/edit.html',user=user)

@app.route('/users/<int:user_id>/edit',methods=['POST'])
def edit_form(user_id):
    first = request.form['first_name']
    last = request.form['last_name']
    url = request.form['image_url']
    url = url if url else None

    user = User.query.get(user_id)

    user.first_name = first
    user.last_name = last
    user.image_url = url

    db.session.add(user)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    
    db.session.commit()

    return redirect('/')

