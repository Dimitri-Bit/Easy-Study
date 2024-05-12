from flask import Flask, jsonify, session, request, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from argon2 import PasswordHasher

import json

class Auth_Manager:
    def __init__(self, db_manager):
        self.password_hasher = PasswordHasher()
        self.db_manager = db_manager


    def validate_credentials(self, username, password):
        if len(username) < 3:
            return {"message": "Username must be at least 3 characters long"}
        if len(password) < 8:
            return {"message": "Password must be at least 8 characters long"}
        return None
    

    def register(self):
            request_data = request.get_json()
            username, password = request_data.get('username'), request_data.get('password')
            error_message = self.validate_credentials(username, password)

            if error_message:
                return json.dumps(error_message), 401
            
            if self.db_manager.get_user_by_username(username):
                return json.dumps({"message": "An account with that username already exists"}), 401
            
            hashed_password = self.password_hasher.hash(password)
            self.db_manager.add_user(username, hashed_password)

            return json.dumps({"message": "User successfully created"}), 201
    

    def login(self):
            request_data = request.get_json()
            username, password = request_data.get('username'), request_data.get('password')
            error_message = self.validate_credentials(username, password)

            if error_message:
                return json.dumps(error_message), 401
            
            db_user_query = self.db_manager.get_user_by_username(username)
            db_user_query = list(db_user_query)[0]

            if not db_user_query:
                return json.dumps({"message": "Incorrect username and or password"}), 404

            try:
                self.password_hasher.verify(db_user_query[2], password)
            except:
                return json.dumps({"message": "Incorrect username and or password"}), 404

            access_token = create_access_token(identity=db_user_query[1])
            return json.dumps({"message": "Successfully logged in", "access_token": access_token}), 200