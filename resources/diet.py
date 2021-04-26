import traceback

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from libs.strings import gettext
from models.diet import DietModel
from models.user import UserModel
from schemas.diet import DietSchema

diet_schema = DietSchema()


class Diet(Resource):

    @classmethod
    @jwt_required()
    def get(cls):
        user = UserModel.find_by_id(get_jwt_identity())
        diet = user.diet
        if not diet:
            return {'message': gettext('diet_not_found')}, 404
        return diet_schema.dump(diet), 200

    @classmethod
    @jwt_required()
    def put(cls):
        try:
            diet_data = request.get_json()
            user = UserModel.find_by_id(get_jwt_identity())
            diet = DietModel(user.id, **diet_data)
            diet.save_to_db()
            return {'message': gettext('diet_updated')}, 200
        except:
            traceback.print_exc()
            return {'message': gettext('diet_failed_to_create_or_update')}, 500

    @classmethod
    @jwt_required()
    def delete(cls):
        user = UserModel.find_by_id(get_jwt_identity())
        diet = user.diet
        if not diet:
            return {'message': gettext('diet_not_found')}, 404
        diet.delete_from_db()
        return {'message': gettext('diet_deleted')}, 200
