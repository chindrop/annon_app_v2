from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()
base = db.make_declarative_base(db.Model)

class Annontate(base):
        id = db.Column(db.Integer, primary_key=True)
        data = db.Column(db.String(10))
        date = db.Column(db.String(150))
        audio_name = db.Column(db.String(150))
        user_email = db.Column(db.String(150), db.ForeignKey('user.email'))

        def __init__(self, data, date, user_email, audio_name):
            self.data = data
            self.date = date
            self.user_email = user_email
            self.audio_name = audio_name

        def __repr__(self):
            return f"<Annontate {self.user_email}>"


class BirdSound(base):
    id = db.Column(db.Integer, primary_key=True)
    audio_name = db.Column(db.String(150))

    def __init__(self, audio_name):
        self.audio_name = audio_name

    def __repr__(self):
        return f"<BirdSound {self.audio_name}>"


class User(base, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))