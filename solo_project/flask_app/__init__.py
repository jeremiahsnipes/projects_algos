# This is a Python program that uses the Flask and Flask-Bcrypt libraries.
# It imports 'Flask' and 'Bcrypt' from these libraries.

from flask import Flask
from flask_bcrypt import Bcrypt

# This line creates a new Flask application object.
# It also creates a Bcrypt object that is linked to the Flask app.

app = Flask(__name__)
bcrypt = Bcrypt(app)

# This line sets a secret key for the Flask app.
# This key is used to encrypt sensitive information.

app.secret_key = 'Its_the_principal'

# This line imports two things called 'users' and 'plural(s)' from a module called 'controllers'
# These are likely parts of a web application that the program will use.

from flask_app.controllers import users, user_scripts
