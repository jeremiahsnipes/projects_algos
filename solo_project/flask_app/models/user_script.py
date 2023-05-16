# This line imports the "connectToMySQL" function from the "mysqlconnection"
# module of the "config" package in the "flask_app" package.
from flask_app.config.mysqlconnection import connectToMySQL
# This line imports the "user" module from the "models" package in the "flask_app" package.
from flask_app.models import user
from flask import flash
# This line creates a variable called "db" and sets it to the string "user_scripts".
db = "ducky_crypt"
class user_script:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.script_name = db_data['script_name']
        self.description = db_data['description']
        self.release_date = db_data['release_date']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.creator = None


    # This line defines the "get_all" method of the "user_script" class.
    @classmethod
    def get_all(cls):
        # This line defines a SQL query to retrieve all user_scripts and their creators from the database.
        query = """
                SELECT * FROM user_scripts
                JOIN users on user_scripts.user_id = users.id;
                """
        # This line executes the SQL query and stores the results in the "results" variable.
        results = connectToMySQL(db).query_db(query)
        # This line creates an empty list to store the user_script objects.
        user_scripts = []
        # This line loops through the results and creates a user_script object for each row in the results.
        for row in results:
            # This line creates a user_script object using the "cls" argument, which is the "user_script" class itself.
            this_user_script = cls(row)
            # This line creates a dictionary containing the user data for the creator of the user_script.
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            # This line creates a user object using the "user" module and the user data dictionary.
            this_user_script.creator = user.User(user_data)
            # This line appends the user_script object to the "user_scripts" list.
            user_scripts.append(this_user_script)
        # This line returns the "user_scripts" list.
        return user_scripts
    # This line defines the "get_by_id" method of the "user_script" class.
    @classmethod
    def get_by_id(cls,data):
        # This line defines a SQL query to retrieve a user_script and its creator from the database, based on the ID passed in as an argument.
        query = """
                SELECT * FROM user_scripts
                JOIN users on user_scripts.user_id = users.id
                WHERE user_scripts.id = %(id)s;
                """
        result = connectToMySQL(db).query_db(query,data)
        if not result:
            return False

        result = result[0]
        this_user_script = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        this_user_script.creator = user.User(user_data)
        return this_user_script

    @classmethod
    def save(cls, form_data):
        # This line defines a SQL query to insert a new user_script into the database.
        query = """
                INSERT INTO user_scripts (script_name,description,release_date,user_id)
                VALUES (%(script_name)s,%(description)s,%(release_date)s,%(user_id)s);
                """
        return connectToMySQL(db).query_db(query,form_data)

    @classmethod
    def update(cls,form_data):
        # This line defines a SQL query to update an existing user_script in the database.
        query = """
                UPDATE user_scripts
                SET script_name = %(script_name)s,
                description = %(description)s,
                release_date = %(release_date)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,form_data)
    
    @classmethod
    def destroy(cls,data):
        query = """
                DELETE FROM user_scripts
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,data)
    
# This line defines the "validate_user_script" method of the "user_script" class.
    @staticmethod
    def validate_user_script(form_data):
        # This line sets "is_valid" to True.
        is_valid = True
        # These lines check if the input data for the user_script is valid or not, and set "is_valid" to False if it's not.
        if len(form_data['script_name']) < 3:
            # This line shows a message using the "flash" function if the name is less than 3 characters long.
            flash("Name must be at least 3 characters long.")
            is_valid = False
        if len(form_data['description']) < 3:
            # This line shows a message using the "flash" function if the description is less than 3 characters long.
            flash("Description must be at least 3 characters long.")
            is_valid = False
        if form_data['release_date'] == '':
            # This line shows a message using the "flash" function if the date_made is not input.
            flash("Please input a date.")
            is_valid = False

        # This line returns "is_valid".
        return is_valid
