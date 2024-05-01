from flask import Flask, jsonify, session, request, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from modules.database.db import Database_Manager
from argon2 import PasswordHasher
import json

__SALT__ = '1531432'

app = Flask(__name__)
db_manager = Database_Manager('db.db', __SALT__)
password_hasher = PasswordHasher()

app.config['SECRET_KEY'] = 'temp_will_move_to_env'
app.config['JWT_SECRET_KEY'] = 'temp_will_move_to_env'
app.config['JWT_TOKEN_LOCATION'] = ['headers']

jwt = JWTManager(app)


def get_hashed_pass(password):
    hash_pass = password_hasher.hash(password)
    return hash_pass


@app.route("/register", methods=["POST"])
def register():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']

    if len(username) < 3:
        return json.dumps({"message": "Username must be longer then 2 characters"}), 401

    if len(password) < 8:
        return json.dumps({"message": "Password must be longer then 7 characters"}), 401
    
    db_user = db_manager.get_user_by_username(username)

    if db_user:
        return json.dumps({"message": "An account with that username already exists"}), 401
    
    db_manager.add_user(username, get_hashed_pass(password))
    return json.dumps({"message": "User successfully created"}), 201


@app.route('/login', methods=['POST'])
def login():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']

    if len(username) < 3:
        return json.dumps({"message": "Username must be longer then 2 characters"}), 401

    if len(password) < 8:
        return json.dumps({"message": "Password must be longer then 7 characters"}), 401
    
    db_user = db_manager.get_user_by_username(username)

    if not db_user: # Don't let the user know which credential is incorrect (incorrect username)
        return json.dumps({"message": "Incorrect username and or password"}), 404
    
    user = list(db_user)[0]

    if not get_hashed_pass(user[2]) == get_hashed_pass(password): # Don't let the user know which credential is incorrect (incorrect password)
        return json.dumps({"message": "Incorrect username and or password"}), 404
    
    access_token = create_access_token(identity=user[1])
    return json.dumps({"message": "Successfully logged in", "access_token": access_token}), 200


if __name__ == "__main__":
    app.run(port=8080)