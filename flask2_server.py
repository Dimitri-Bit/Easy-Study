from flask import Flask, jsonify, session, request, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from modules.database.db import Database_Manager
from argon2 import PasswordHasher
import json
import modules.models.user as user_model

__SALT__ = '1531432'

app = Flask(__name__)

db_manager = Database_Manager('db.db', __SALT__)
password_hasher = PasswordHasher()

app.config['SECRET_KEY'] = 'temp_will_move_to_env'
app.config['JWT_SECRET_KEY'] = 'temp_will_move_to_env'
app.config['JWT_TOKEN_LOCATION'] = ['headers']

jwt = JWTManager(app)

def validate_credentials(username, password):
    if len(username) < 3:
        return {"message": "Username must be at least 3 characters long"}
    if len(password) < 8:
        return {"message": "Password must be at least 8 characters long"}
    return None


@app.route("/register", methods=["POST"])
def register():
    request_data = request.get_json()
    username, password = request_data.get('username'), request_data.get('password')
    error_message = validate_credentials(username, password)

    if error_message:
        return json.dumps(error_message), 401
    
    if db_manager.get_user_by_username(username):
        return json.dumps({"message": "An account with that username already exists"}), 401
    
    hashed_password = password_hasher.hash(password)
    db_manager.add_user(username, hashed_password)

    return json.dumps({"message": "User successfully created"}), 201


@app.route('/login', methods=['POST'])
def login():
    request_data = request.get_json()
    username, password = request_data.get('username'), request_data.get('password')
    error_message = validate_credentials(username, password)

    if error_message:
        return json.dumps(error_message), 401
    
    db_user_query = db_manager.get_user_by_username(username)

    if not db_user_query:
        return json.dumps({"message": "Incorrect username and or password"}), 404

    db_user = user_model.mapUser(list(db_user_query)[0])
    
    try:
        password_hasher.verify(db_user.password, password)
    except:
        return json.dumps({"message": "Incorrect username and or password"}), 404

    access_token = create_access_token(identity=db_user.id)
    return json.dumps({"message": "Successfully logged in", "access_token": access_token}), 200


if __name__ == "__main__":
    app.run(port=8080)