from os import getenv, urandom
import io
import random
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, render_template_string
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash
from flask_toastr import Toastr
from flask_cors import CORS
from flask_login import login_user, current_user, logout_user, LoginManager
import matplotlib.pyplot as plt
import numpy as np
import wave
from datetime import date
from models import db, User, Annontate
from s3_helpers import configure_boto

load_dotenv()


def configure_app(application):
    # configurations
    configure = {
        "development": "config.devConfig",
        "production": "config.prodConfig",
        "staging": "config.stageConfig",
        "testing": "config.testConfig"
    }

    # Determine the configuration file to read using environment variables
    config_name = getenv('FLASK_CONFIGURATION', 'development')
    # Read settings as objects
    application.config.from_object(configure[config_name])
    return application.config


def create_app():
    app = Flask(__name__)
    configure_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    # migrate = Migrate(app, db)
    toastr = Toastr(app)
    cors = CORS(app, resources=r"/*")
    boto_session, bucket, s3_client = configure_boto()
    app.secret_key = urandom(24)
    login_manager = LoginManager()
    login_manager.init_app(app)

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
            return redirect(url_for('annotate_page'))
        else:
            flash('login fail, check your password and email entered', 'warning')
            return render_template('login.html')

    @app.route("/annotate_page")
    def annotate_page():
        random_file = get_random_file()
        read_audio(random_file[1])
        return render_template('annotate_page.html', url='/static/specto/new_plot.png', random_file_link=random_file[0])

    @app.route("/logout")
    def logout():
        logout_user()
        return render_template('home.html')

    @app.route("/anwser_yes")
    def anwser_yes():
        store_answer("Yes")
        return annotate_page()

    @app.route("/anwser_no")
    def anwser_no():
        store_answer("no")
        return annotate_page()

    @app.route("/anwser_maybe")
    def anwser_maybe():
        store_answer("maybe")
        return annotate_page()

    def store_answer(the_answer):
        today = date.today()
        new_date = today.strftime("%d/%m/%Y")
        new_annontate = Annontate(
            data=the_answer, date=new_date, user_email=current_user.email, audio_name=request.args.get("filename"))
        db.session.add(new_annontate)
        db.session.commit()

    def read_audio(random_file):
        wav_file = wave.open(random_file, 'r')
        signal = wav_file.readframes(-1)
        signal = np.frombuffer(signal, dtype='int16')
        # gets the frame rate
        frame_rate = wav_file.getframerate()

        plot_waveform(signal, frame_rate)
        plot_spectrogram(signal, frame_rate)

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

    def get_random_file():
        file_names = [file.key for file in bucket.objects.all()]
        chosen_file = random.choice(file_names)
        random_file_link = s3_client.generate_presigned_url(
            'get_object', ExpiresIn=3600, Params={'Bucket': bucket.name, 'Key': chosen_file})
        random_file = bucket.Object(chosen_file)
        random_file = random_file.get()['Body']
        return random_file_link, random_file

    return app


blackbird = create_app()

if __name__ == "__main__":
    blackbird.run()
