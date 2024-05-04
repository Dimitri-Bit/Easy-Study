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
    
    hashed_password = password_hasher.hash(password)
    db_manager.add_user(username, hashed_password)

    return json.dumps({"message": "User successfully created"}), 201


@app.route('/login', methods=['POST'])
def login():
    request_data = request.get_json()
    username, password = request_data['username'], request_data['password']

    if len(username) < 3:
        return json.dumps({"message": "Username must be at least 3 characters long"}), 401
    if len(password) < 8:
        return json.dumps({"message": "Password must be at least 8 characters long"}), 401
    
    db_user_query = db_manager.get_user_by_username(username)

    if not db_user_query:
        return json.dumps({"message": "Incorrect username and or password1"}), 404
    
    db_user = list(db_user_query)[0]
    db_user_password = db_user[2]

    try:
        password_hasher.verify(db_user_password, password)
    except:
        return json.dumps({"message": "Incorrect username and or password2"}), 404

    access_token = create_access_token(identity=db_user[1])
    return json.dumps({"message": "Successfully logged in", "access_token": access_token}), 200


if __name__ == "__main__":
    app.run(port=8080)