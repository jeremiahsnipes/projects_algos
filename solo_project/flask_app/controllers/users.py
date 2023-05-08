# Import the Flask app and other necessary modules
from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User

# Flask app route for the index page, which redirects to the login page
@app.route('/')
def index():
    return redirect('/user/login')

# Flask app route for the login page
@app.route('/user/login')
def login():
    # Check if a user is already logged in and redirect to the dashboard page if true
    if 'user_id' in session:
        return redirect('/dashboard')

    # Render the login template if user is not logged in
    return render_template('index.html')

# Flask app route for processing login form data
@app.route('/user/login/process', methods=['POST'])
def login_success():
    # Validate login information provided in the login form
    user = User.validate_login(request.form)
    # Redirect to the login page if validation fails
    if not user:
        return redirect('/user/login')

    # Set user session variable to the user id if validation succeeds
    session['user_id'] = user.id
    return redirect('/dashboard')

# Flask app route for processing registration form data
@app.route('/user/register/process', methods=['POST'])
def register_success():
    # Validate registration information provided in the registration form
    if not User.validate_reg(request.form):
        return redirect('/user/login')

    # Save user registration information to the database
    user_id = User.save(request.form)
    # Set user session variable to the user id
    session['user_id'] = user_id
    return redirect('/dashboard')

# Flask app route for logging out the current user
@app.route('/user/logout')
def logout():
    # Remove the user session variable if it exists
    if 'user_id' in session:
        session.pop('user_id')
    return redirect('/user/login')
