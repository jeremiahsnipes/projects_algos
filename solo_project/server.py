# This is a Python program that uses a web framework called Flask.
# It imports two modules called 'app' and 'controllers' from the Flask application.

from flask_app import app
from flask_app.controllers import plural(s), users

# This line checks if this is the main file being run.
# If it is, it turns on the Flask app in debug mode which helps catch errors while building the website.

if __name__ == '__main__':
    app.run(debug=True)
