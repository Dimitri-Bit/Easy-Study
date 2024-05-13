from flask import Flask, jsonify, session, request, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt

from db import Database_Manager
from auth import Auth_Manager
from lecture import Lecture_Manager

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

db_manager = Database_Manager('/home/batman/Documents/Easy-Study/db.db')
auth_manager = Auth_Manager(db_manager)
lecture_manager = Lecture_Manager(db_manager, os.getenv('OPENAI_API_KEY'))

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

@app.route('/addlecture', methods=['POST'])
@jwt_required()
def add_lecture():
    lecture_results = lecture_manager.new_lecture()
    return lecture_results


@app.route('/getlectures', methods=['GET'])
@jwt_required()
def get_lectures():
    lecture_results = lecture_manager.get_lectures()
    return lecture_results


if __name__ == "__main__":
    app.run(port=8080)