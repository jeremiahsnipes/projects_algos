from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import bcrypt
import re

db = "recipes"
EMAIL_REGEX = re.compile(r'''
    ^                  # Start of the string
    [a-zA-Z0-9.+_-]+   # Username, can contain letters, digits, plus sign, underscore, or hyphen
    @                  # At symbol
    [a-zA-Z0-9._-]+    # Domain name, can contain letters, digits, period, underscore, or hyphen
    \.                 # Dot
    [a-zA-Z]+          # Top-level domain, can contain letters only
    $                  # End of the string
''', re.VERBOSE)
class User:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.email = db_data['email']
        self.password = db_data['password']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

# In the save() method, the user's password is hashed using the generate_password_hash() 
# function from bcrypt. This function takes a plain text password and generates a hash of 
# that password that can be safely stored in a database. The hashed 
# password is then included in the data that is sent to the database to create a new user.

    @classmethod
    def save(cls,form_data):
        hashed_data = {
            'first_name': form_data['first_name'],
            'last_name': form_data['last_name'],
            'email': form_data['email'],
            'password': bcrypt.generate_password_hash(form_data['password']),
        } # Create a dictionary called 'hashed_data' that contains the user's form data along with a hashed version of the password
        query = """ 
                INSERT INTO users (first_name,last_name,email,password)
                VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);
                """ # Define an SQL query string that inserts the user's form data into the 'users' table in the database
        return connectToMySQL(db).query_db(query,hashed_data) # Execute the query using the 'query_db()' method of the 'connectToMySQL()' function, passing in the query string and the 'hashed_data' dictionary as arguments

    @classmethod
    def get_by_email(cls,data):
        query = """
                SELECT * FROM users
                WHERE email = %(email)s;
                """  # Define an SQL query string that retrieves user data from the 'users' table in the database based on the given email
        result = connectToMySQL(db).query_db(query,data)  # If a user with the given email exists, create a new instance of the 'User' class with the retrieved data and return it
        if not result:
            return False

        return cls(result[0])

    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM users
                WHERE id = %(id)s;
                """ # Define an SQL query string that retrieves user data from the 'users' table in the database based on the given id
        result = connectToMySQL(db).query_db(query,data) # Execute the query using the 'query_db()' method of the 'connectToMySQL()' function, passing in the query string and the 'data' dictionary as arguments
        if not result:
            return False

        return cls(result[0])  # If a user with the given id exists, create a new instance of the 'User' class with the retrieved data and return it

# This method checks the validation for registration form data.
# It receives the form data as an argument.
    @staticmethod
    def validate_reg(form_data):
        is_valid = True
        # If the email field is empty, it sets is_valid to False and flashes an error message.
        if len(form_data['email']) < 1:
            flash("Email cannot be blank.","register")
            is_valid = False
        # If the email field does not match the email pattern, it sets is_valid to False and flashes an error message.
        elif not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid email address.","register")
            is_valid = False
        # If the email field already exists in the database, it sets is_valid to False and flashes an error message.
        elif User.get_by_email(form_data):
            flash("A user already exists for that email.","register")
            is_valid = False
        # If the password field is less than 8 characters, it sets is_valid to False and flashes an error message.
        if len(form_data['password']) < 8:
            flash("Password must be at least 8 characters long.","register")
            is_valid = False
        # If the password and confirm_password fields do not match, it sets is_valid to False and flashes an error message.
        if form_data['password'] != form_data['confirm_password']:
            flash("Passwords must match.","register")
            is_valid = False
        # If the first name field is less than 3 characters, it sets is_valid to False and flashes an error message.
        if len(form_data['first_name']) < 3:
            flash("First name must be at least 3 characters long.","register")
            is_valid = False
        # If the last name field is less than 3 characters, it sets is_valid to False and flashes an error message.
        if len(form_data['last_name']) < 3:
            flash("Last name must be at least 3 characters long.","register")
            is_valid = False
        # Finally, it returns is_valid.
        return is_valid

    @staticmethod
    def validate_login(form_data):
        # If the email field does not match the email pattern, it sets is_valid to False and flashes an error message.
        if not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid email/password.","login")
            return False

        # It calls the get_by_email() method of the User class to retrieve the user with the given email address.
        user = User.get_by_email(form_data)

        # If the email does not exist in the database, it sets is_valid to False and flashes an error message.
        if not user:
            flash("Invalid email/password.","login")
            return False
        
        # It uses the check_password_hash() method of the bcrypt module to compare the hashed password with the plain text password entered by the user.
        if not bcrypt.check_password_hash(user.password, form_data['password']):
            flash("Invalid email/password.","login")
            return False
        
        # If the passwords match, it returns the user object.
        return user

    
# In the validate_login() method, the hashed password that was previously stored 
# in the database is retrieved and compared to the plain text password that the 
# user entered when logging in. This is done using the check_password_hash() function 
# from bcrypt. If the two passwords match, then the user is authenticated and the User 
# object representing that user is returned. If the passwords do not match, then the user 
# is not authenticated and an error message is displayed.