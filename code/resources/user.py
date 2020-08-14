from flask_restful import Resource, reqparse
from models.user import UserModel
import sqlite3

class UserRegister(Resource):
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

    def post(self):
        # Collect the data from JSON payload.
        data = UserRegister.parser.parse_args()

        # Check for and prevent duplicate usernames.
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201