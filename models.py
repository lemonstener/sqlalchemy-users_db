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
        db.String,
        nullable = False
    )

    last_name = db.Column(
        db.String,
        nullable = False
    )

    image_url = db.Column(
        db.String,
        unique = True
    )

    def __repr__(self):
        u = self
        return f'<User id={u.id} first_name = {u.first_name} last_name = {u.last_name} image_url = {u.image_url}>'

    def full_name(self):
        u = self
        return f'{u.first_name} {u.last_name}'

    