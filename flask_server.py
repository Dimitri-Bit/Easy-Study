import json
from flask import Flask, request
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from modules.auth.user import User
from modules.database.db import Database_Manager


app = Flask(__name__)
database_manager = Database_Manager()


app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route("/login", methods=["POST"])
def login():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']

    db_user = database_manager.get_user_by_username(username)
    
    if not db_user:
        return json.dumps({"message": "Account with that username does not exist"}), 404
    
    db_user = list(db_user)[0]

    if not db_user['password'] == password:
        return json.dumps({"message": "Incorrect username or password"}), 401
                
    user = User(int(db_user['id']), db_user['username'], db_user['password'])
    login_user(user)
    return json.dumps({"message": "You have logged in"})
    

if __name__ == "__main__":
    app.run(port=8080)