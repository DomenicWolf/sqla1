"""Blogly application."""

from flask import Flask,render_template,redirect,request,session,flash
from models import db, connect_db,User,Post,Tag,PostTag
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


@app.route('/users/<int:user_id>/posts/form')
def post_form(user_id):
    user = User.query.get(user_id)
    
    return render_template('pform.html',user=user)


@app.route('/users/<int:user_id>/posts/new',methods=['POST'])
def create_post(user_id):
    title = request.form['title']
    content = request.form['content']
    id = user_id
    new=Post(title=title,content=content,user_id=id)
    db.session.add(new)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_posts(post_id):
    post = Post.query.get(post_id)
    return render_template('post.html',post=post)

#@app.route('/posts/<int:post_id>/edit')
#def edit_posts(post_id):
    

@app.route('/posts/<int:post_id>/edit', methods=['POST','GET'])
def edit_posts(post_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post = Post.query.get(post_id)
        post.title = title
        post.content = content
        db.session.commit()
        return redirect(f'/posts/{post_id}')
    else:
        post = Post.query.get(post_id)
        return render_template('pedit.html',post=post)

@app.route('/posts/<int:post_id>/delete')
def delete_posts(post_id):
    post = Post.query.get(post_id)
    Post.query.filter_by(id=post_id).delete()

    db.session.commit()

    return redirect(f'/users/{post.user_id}')

@app.route('/tags')
def show_tags():
    tags = Tag.query.all()
    return render_template('tags.html',tags=tags)

@app.route('/tags/<int:id>')
def show_tag_detail(id):
    tag = Tag.query.get(id)
    posts = tag.posts
    return render_template('tag_details.html',tag=tag,posts=posts)

@app.route('/tags/new',methods=['POST','GET'])
def create_tag_form():
    if request.method=='GET':
        return render_template('tform.html')
    else:
        name=request.form['name']
        new_tag = Tag(name=name)
        db.session.add(new_tag)
        db.session.commit()
        return redirect('/tags')
    
@app.route('/tags/<int:id>/edit',methods=['POST', 'GET'])
def edit_tag(id):
    if request.method=='GET':
        return render_template('edit_tag.html',id=id)
    else:
        name=request.form['name']
        tag = Tag.query.get(id)
        tag.name = name
        
        db.session.commit()
        return redirect('/tags')
    
@app.route('/tags/<int:id>/delete')
def delete_tag(id):
    Tag.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/tags')



