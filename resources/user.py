import traceback

from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, \
    get_jwt_identity
from flask_restful import Resource
from werkzeug.security import safe_str_cmp

from blacklist import BLACKLIST
from libs.strings import gettext
from models.user import UserModel
from schemas.user import UserSchema

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)
        if UserModel.find_by_username(user.username):
            return {'message': gettext('user_username_already_exists')}, 400
        try:
            user.save_to_db()
            return {'message': gettext('user_registered')}, 201
        except:
            traceback.print_exc()
            user.delete_from_db()
            return {'message': gettext('user_failed_to_create')}, 500


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': gettext('user_not_found')}, 404
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': gettext('user_not_found')}, 404
        user.delete_from_db()
        return {'message': gettext('user_deleted')}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json)
        user = UserModel.find_by_username(user_data.username)
        if user and safe_str_cmp(user.password, user_data.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_access_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': gettext('user_invalid_credentials')}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_jwt()['jti']
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        BLACKLIST.add(jti)
        return {
            'message': gettext('user_logged_out').format(user.username)
        }, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200


class ChangePassword(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json)
        user = UserModel.find_by_username(user_data.username)
        if not user:
            return {'message': gettext('user_not_found')}, 404
        user.password = user_data.password
        user.save_to_db()
        return {'message': gettext('user_password_updated')}, 201
