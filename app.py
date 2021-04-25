from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api
from marshmallow import ValidationError

from blacklist import BLACKLIST
from db import db
from ma import ma
from resources.user import UserRegister, UserLogin, User, TokenRefresh, \
    UserLogout, ChangePassword

load_dotenv()

app = Flask(__name__)
app.config.from_object('default_config')
app.config.from_envvar('APPLICATION_SETTINGS')
api = Api(app)
jwt = JWTManager(app)
db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_error(err):
    return jsonify(err.message), 400


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


api.add_resource(UserRegister, '/sign-up')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(ChangePassword, '/user/password')
api.add_resource(TokenRefresh, '/refresh')


if __name__ == '__main__':
    app.run(port=5000)
