# BLACKBIRD ANNOTATION TOOL
Blackbird Annotation Tool is a web application which lets its users to upload, listen, visualise and most importantly **annotate** audio recordings. The main purpose is to provide a way to produce and record metadata for the field recorded bird sounds. So that these can be aggragated with the machine learning applications in the future for scientific purposes. The web application is written in Python 3.10 using Flask 2.0 as framework. It is served as a multi-container Docker application together with a Postgres database and a PGAdmin4 interface. This documentation is aimed for future users and contributers. It consists an explanation to backend architecture.

### Structure
```
.github                      
-- workflows
   |   |-- blackbirdcicd.yml #github workflows definiton
.gitignore                   #files to be exempt from git
Docker-compose.yaml          #container and service definitions for docker-compose
Dockerrun.aws.json           #docker-compose translated to json for aws-eb deploy
README.md                    # you are here
app                          #source folder for the flask app
   |-- .dockerignore         # files to be exempt from docker
   |-- app.py                # source file for the flask app
   |-- config.py             # configuration file for the flask app
   |-- dockerfile            # configuration file for the docker container of flask app
   |-- example.env           # .env file template to set environment variables
   |-- models.py             # Object relation models for DB
   |-- s3_helpers.py         # Functions related to aws s3 configuration
   |-- static                # static files for the flask app
   |   |-- css             
   |   |   |-- style.css     # frontend styling (idle for now)
   |   |-- images            # folder where audio file plotes saved
   |   |   |-- new_plot.png  
   |   |-- specto            #folder where spectogram images saved
   |   |   |-- new_plot.png
   |-- templates             # html files for the pages
   |   |-- annontate_page.html
   |   |-- base.html
   |   |-- home.html
   |   |-- login.html
   |   |-- sign_up.html
upload_files.py             # a standalone script to upload audio files to s3 server
```

### Functions & Routes
Most of the relevant functions for the application are defined in the app.py file. It will be exclusivly implied if it has been defined somewhere else.

- **configure-app(application):** configures the flask application (argument) with the settings from config.py based on "FLASK_CONFIGURATION" environment variable. Defaults to development if its not defined.
- **create_app():** The factory function for flask application. it initiates additional libraries like Toastr, Boto, LoginManager and initiates the app and the database based on predefined models from models.py. Then it defines app routes and utility functions.
- **load_user():** returns a user object to satisfy FLask-Login requirements
- **register():** renders registration page and retrieves form-data from registration page. It creates a new user if requirements are satisfied and redirects to the login page. It flashes errors messages if user already exists or two given passwords doesnt match.
- **login_submit():** renders login page and checks provided login data with database. Redirects to the annotation page if succesful and displays an error if not.
- **annotate_page():** renders annotation page and calls functions to get a random audio file and to renders related graphs
- **logout():** logs user out and renders homepage
- **answer_yes() & answer_no() & answer_maybe():** calls the function to record given answer and redirects to annotate_page 
-  **store_answer(the_answer):** records the answer to the database
-  **read_audio(random_file):** opens audio file as a stream, detects its frame rate and calls the fuctions to plot it.
- **plot_waveform(signal, f_rate):** takes a signal stream and its frame rate as arguments. Plots a waveform graph and saves it as image
- **plot_spectogram()signal, f_rate):** takes a signal stream and its frame rate as arguments. Plots a spectogram graph from it and saves it as image.
-  **get_random_file():** returns a random file from s3 server and a presigned url for it which expires in an hour.





