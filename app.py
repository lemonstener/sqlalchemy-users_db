from flask import Flask, request, render_template, flash, redirect, sessions
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'chickenz'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

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
        flash('First and last names cannot be null')
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
        flash('First and last names cannot be null')
        db.session.rollback()
        return redirect(f'/users/{user_id}/edit')
 
    if len(user.image_url) == 0:
        user.image_url = 'https://www.travelcontinuously.com/wp-content/uploads/2018/04/empty-avatar.png'
    
    db.session.add(user)
    db.session.commit()

    return redirect(f'/users/{user.id}')  
    

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/users')