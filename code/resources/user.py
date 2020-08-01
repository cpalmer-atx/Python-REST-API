from flask_restful import Resource, reqparse
from models.user import UserModel
import sqlite3

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
        if UserModel.find_by_username(data['username']):
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