# Import the Flask app and other necessary modules
from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user_script import user_script
from flask_app.models.user import User


# Flask app route for the dashboard page
@app.route('/dashboard')
def dashboard():
    # Redirect to the login page if user is not logged in
    if 'user_id' not in session:
        return redirect('/user/login')
    # Get user by id from the session
    user = User.get_by_id({"id":session['user_id']})
    # Redirect to the logout page if user is not found in the database
    if not user:
        return redirect('/user/logout')
    # Render the dashboard template with user and user_script data
    return render_template('dashboard.html', user=user, user_scripts=user_script.get_all())

# Flask app route for the user_script creation page
@app.route('/user_scripts/new')
def create_user_script():
    # Redirect to the login page if user is not logged in
    if 'user_id' not in session:
        return redirect('/user/login')
    # Render the user_script_new template
    return render_template('user_script_new.html')

# Flask app route for processing user_script creation form data
@app.route('/user_scripts/new/process', methods=['POST'])
def process_user_script():
    # Redirect to the login page if user is not logged in
    if 'user_id' not in session:
        return redirect('/user/login')
    # Validate user_script information provided in the user_script creation form
    if not user_script.validate_user_script(request.form):
        return redirect('/user_scripts/new')
    # Save user_script information to the database
    data = {
        'user_id': session['user_id'],
        'script_name': request.form['script_name'],
        'description': request.form['description'],
        'release_date': request.form['release_date'],
    }
    user_script.save(data)
    return redirect('/dashboard')

# Flask app route for viewing a single user_script
@app.route('/user_scripts/<int:id>')
def view_user_script(id):
    # Redirect to the login page if user is not logged in
    if 'user_id' not in session:
        return redirect('/user/login')
    # Render the user_script_view template with user_script data by id
    return render_template('user_script_view.html',user_script=user_script.get_by_id({'id': id}))

# Flask app route for editing a single user_script
@app.route('/user_scripts/edit/<int:id>')
def edit_user_script(id):
    # Redirect to the login page if user is not logged in
    if 'user_id' not in session:
        return redirect('/user/login')
    # Render the user_script_edit template with user_script data by id
    return render_template('user_script_edit.html',user_script=user_script.get_by_id({'id': id}))

# Flask app route for processing user_script editing form data
@app.route('/user_scripts/edit/process/<int:id>', methods=['POST'])
def process_edit_user_script(id):
    # Redirect to the login page if user is not logged in
    if 'user_id' not in session:
        return redirect('/user/login')
    # Validate user_script information provided in the user_script editing form
    if not user_script.validate_user_script(request.form):
        return redirect(f'/user_scripts/edit/{id}')
    # Update user_script information in the database by id
    data = {
        'id': id,
        'script_name': request.form['script_name'],
        'description': request.form['description'],
        'release_date': request.form['release_date'],
    }
    user_script.update(data)
    return redirect('/dashboard')

# Flask app route for deleting a single user_script
@app.route('/user_scripts/destroy/<int:id>')
def destroy_user_script(id):
    # Redirect to the login page if user is not logged in
    if 'user_id' not in session:
        return redirect('/user/login')
    # Delete user_script information from the database by id
    user_script.destroy({'id':id})
    return redirect('/dashboard')