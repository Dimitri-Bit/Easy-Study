import json
from flask import Flask, request
from flask_login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user
from modules.auth.user import User

app = Flask(__name__)


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
    user = User(1, username, password)

    login_user(user)
    print(login_user)

    return json.dumps({"success": "You have logged in"}), 200
    

if __name__ == "__main__":
    app.run(port=8080)