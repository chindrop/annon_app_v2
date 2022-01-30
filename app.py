import os
import random
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash
from flask_toastr import Toastr
from flask_cors import CORS
from flask_login import UserMixin, login_user, current_user, logout_user, LoginManager
import matplotlib.pyplot as plt
import numpy as np
import wave
import os.path
from datetime import date


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://chinlee5:password@localhost:5432/annontation'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
toastr = Toastr(app)
cors = CORS(app, resources=r"/*")
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)


class Annontate(db.Model):
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


class BirdSound(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    audio_name = db.Column(db.String(150))

    def __init__(self, audio_name):
        self.audio_name = audio_name

    def __repr__(self):
        return f"<BirdSound {self.audio_name}>"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    def __init__(self, email, password, first_name):
        self.first_name = first_name
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<User {self.email}>"

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signup")
def signup():
    return render_template("sign_up.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    email = request.form['email']
    first_name = request.form['firstName']
    password1 = request.form['password1']
    password2 = request.form['password2']
    print(first_name)
    print(password1)
    if password1 == password2:
        password_hash = generate_password_hash(password1)
        existing_user = User.query.filter_by(email=email).first()
        if existing_user is None:
            new_user = User(email=email, first_name=first_name,
                            password=password_hash)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created', 'success')
            return redirect(url_for('login'))
        else:
            flash('Account already exist')
            return redirect(url_for('signup'))
    else:
        flash('Password does not match')
        return redirect(url_for('signup'))


@app.route('/login_submit', methods=["GET", "POST"])
def login_submit():
    email_entered = request.form['email']
    password_entered = request.form['password']
    user = User.query.filter_by(email=email_entered).first()
    if user is not None and check_password_hash(user.password, password_entered):
        login_user(user, remember=True)
        return redirect(url_for('annontate_page'))
    else:
        flash('login fail, check your password and email entered', 'warning')
        return render_template('login.html')


def read_audio(random_file):
    raw = wave.open(
        "static/subsample_wavs/" + random_file, "r")
    # Extract Raw Audio from Wav File
    signal = raw.readframes(-1)
    signal = np.frombuffer(signal, dtype="int16")
    # gets the frame rate
    f_rate = raw.getframerate()

    plot_waveform(signal, f_rate)
    plot_spectrogram(signal, f_rate)


def plot_waveform(signal, f_rate):
    time = np.linspace(
        0,  # start
        len(signal) / f_rate,
        num=len(signal)
    )
    fig, ax = plt.subplots()
    plt.title("Sound Wave")
    ax.set_xlabel("Time (s)")
    ax.plot(time, signal)
    fig.savefig('static/images/new_plot.png')


def plot_spectrogram(signal, f_rate):
    time = np.linspace(
        0,  # start
        len(signal) / f_rate,
        num=len(signal)
    )
    fig, ax = plt.subplots()
    ax.set_xlabel("Time (s)")
    ax.specgram(signal, Fs=f_rate)
    fig.savefig('static/specto/new_plot.png')



# def visualize(random_file):
#    y=read_audio(random_file)
#    plot_spectrogram(y)


@app.route("/annontate_page")
def annontate_page():
    random_file = random.choice(os.listdir("static/subsample_wavs"))
    read_audio(random_file)
    return render_template('annontate_page.html', url='/static/specto/new_plot.png', random_file=random_file)


@app.route("/logout")
def logout():
    logout_user()
    return render_template('home.html')


@app.route("/anwser_yes")
def anwser_yes():
    random_file = random.choice(os.listdir(
        "static/subsample_wavs"))
    read_audio(random_file)
    today = date.today()
    new_date = today.strftime("%d/%m/%Y")
    new_annontate = Annontate(
        data='Yes', date=new_date, user_email=current_user.email, audio_name=random_file)
    db.session.add(new_annontate)
    db.session.commit()
    return render_template('annontate_page.html', url='/static/specto/new_plot.png', random_file=random_file)


@app.route("/anwser_no")
def anwser_no():
    random_file = random.choice(os.listdir(
        "static/subsample_wavs"))
    read_audio(random_file)
    today = date.today()
    new_date = today.strftime("%d/%m/%Y")
    new_annontate = Annontate(
        data='no', date=new_date, user_email=current_user.email, audio_name=random_file)
    db.session.add(new_annontate)
    db.session.commit()
    return render_template('annontate_page.html', url='/static/specto/new_plot.png', random_file=random_file)


@app.route("/anwser_maybe")
def anwser_maybe():
    random_file = random.choice(os.listdir(
        "static/subsample_wavs"))
    read_audio(random_file)
    today = date.today()
    new_date = today.strftime("%d/%m/%Y")
    new_annontate = Annontate(
        data='maybe', date=new_date, user_email=current_user.email, audio_name=random_file)
    db.session.add(new_annontate)
    db.session.commit()
    return render_template('annontate_page.html', url='/static/specto/new_plot.png', random_file=random_file)


if __name__ == "__main__":
    app.run(debug=True)
