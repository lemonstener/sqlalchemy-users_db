from flask import Flask, request, render_template, flash, redirect, sessions
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'chickenz'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


# USERS

@app.route('/')
def redirect_to_users():
    return redirect('/users')

@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('home.html',users=users)

@app.route('/users/<int:user_id>')
def user_details(user_id):
    user = User.query.get(user_id)
    return render_template('user.html',user=user)

@app.route('/users/new')
def new_user():
    return render_template('new.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    first_name = request.form['first']
    last_name = request.form['last']
    image_url = request.form['url']
    image_url = image_url if image_url else None

    if len(first_name) == 0 or len(last_name) == 0:
        flash('First and last names cannot be empty')
        db.session.rollback()
        return redirect(f'/users/new')

    new_user = User(first_name=first_name,last_name=last_name,image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = User.query.get(user_id)
    return render_template('edit.html',user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    user = User.query.get(user_id)
    user.first_name = request.form['first']
    user.last_name = request.form['last']
    user.image_url = request.form['url']

    if len(user.first_name) == 0 or len(user.last_name) == 0:
        flash('First and last names cannot be empty')
        db.session.rollback()
        return redirect(f'/users/{user_id}/edit')
 
    if len(user.image_url) == 0:
        user.image_url = 'https://www.travelcontinuously.com/wp-content/uploads/2018/04/empty-avatar.png'
    
    db.session.add(user)
    db.session.commit()

    return redirect(f'/users/{user.id}')  
    
@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')


# POSTS

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    return render_template('post.html',post=post,tags=tags)

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('/post-new.html',user=user,tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def new_post(user_id):
    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist('tags')

    if len(title) == 0 or len(content) == 0:
        flash('Title and content cannot be empty')
        db.session.rollback()
        return redirect(f'/users/{user_id}/posts/new')

    post = Post(title=title,content=content,user_id=user_id)
    db.session.add(post)
    db.session.commit()

    for num in tags:
        tag = PostTag(post_id=post.id,tag_id=num)
        db.session.add(tag)
        db.session.commit()
    
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('post-edit.html',post=post,tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    if len(post.title) == 0 or len(post.content) == 0:
        flash('Title and content cannot be empty')
        db.session.rollback()
        return redirect(f'/posts/{post_id}/edit')
        
    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.id}')  

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')


# TAGS

@app.route('/tags')
def show_tags():
    tags = Tag.query.all()
    return render_template('tags.html',tags=tags)

@app.route('/tags/new')
def show_tag_form():
    return render_template('tag-new.html')

@app.route('/tags/new', methods=['POST'])
def create_tag():
    name = request.form['name']
    tag = Tag(name=name)

    if len(name) == 0:
        flash('Tag name cannot be empty')
        return redirect('/tags/new')

    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag.html',tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag-edit.html',tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    name = request.form['name']
    tag = Tag.query.get_or_404(tag_id)

    if len(name) == 0:
        flash('Tag name cannot be empty')
        return redirect(f'/tags/{tag.id}/edit')

    tag.name = name
    db.session.commit()
    return redirect(f'/tags/{tag.id}')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')
