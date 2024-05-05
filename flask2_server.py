from flask import Flask, jsonify, session, request, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt

from modules.db import Database_Manager
from modules.auth import Auth_Manager

app = Flask(__name__)

db_manager = Database_Manager('db.db')
auth_manager = Auth_Manager(db_manager)

app.config['SECRET_KEY'] = 'temp_will_move_to_env'
app.config['JWT_SECRET_KEY'] = 'temp_will_move_to_env'
app.config['JWT_TOKEN_LOCATION'] = ['headers']

jwt = JWTManager(app)

@app.route("/register", methods=["POST"])
def register():
    auth_results = auth_manager.register()
    return auth_results


@app.route('/login', methods=['POST'])
def login():
    auth_results = auth_manager.login()
    return auth_results


if __name__ == "__main__":
    app.run(port=8080)