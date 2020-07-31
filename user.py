from flask_restful import Resource, reqparse
import sqlite3

class User:

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row is not None:
            user = cls(*row)     # (id, user, password)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row is not None:
            user = cls(*row)     # (id, user, password)
        else:
            user = None

        connection.close()
        return user

class UserRegister(Resource):

    # Tool to parse all requests
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="Username cannot be left blank."
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="Password cannot be left blank."
    ) 
    # END PARSER TOOL

    def post(self):
        # Collect the data from JSON payload.
        data = UserRegister.parser.parse_args()

        # Check for and prevent duplicate usernames.
        if User.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        # Connect to the db and create a cursor.
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # Insert values into the table.
        # id is auto generated and username/password is provided.
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        # Save the changes and close the connection.
        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201