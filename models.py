import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    first_name = db.Column(
        db.Text,
        nullable = False
    )

    last_name = db.Column(
        db.Text,
        nullable = False
    )

    image_url = db.Column(
        db.Text,
        default = 'https://www.travelcontinuously.com/wp-content/uploads/2018/04/empty-avatar.png'
    )

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        u = self
        return f'<User id={u.id} first_name = {u.first_name} last_name = {u.last_name} image_url = {u.image_url}>'

    def full_name(self):
        u = self
        return f'{u.first_name} {u.last_name}'


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(
        db.Integer, 
        primary_key=True,
        autoincrement=True
        )

    title = db.Column(
        db.Text, 
        nullable=False
        )

    content = db.Column(
        db.Text, 
        nullable=False
        )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now
        )

    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id'), 
        nullable=False
        )

    def __repr__(self):
        p = self
        return f'<Post_id = {p.id} title = {p.title} content = {p.content} created_at = {p.created_at} user_id {p.user_id}> '


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    name = db.Column(
        db.Text,
        nullable=False
    )

    posts = db.relationship('Post', secondary='post_tags', backref='tags')


class PostTag(db.Model):
    __tablename__ = 'post_tags'

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id'),
        primary_key=True
    )

    tag_id = db.Column(
        db.Integer,
        db.ForeignKey('tags.id'),
        primary_key=True
    )