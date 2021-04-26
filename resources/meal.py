import traceback
from collections import defaultdict
from datetime import date

from dateutil.utils import today
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from libs.strings import gettext
from models.meal import MealModel
from models.user import UserModel
from schemas.meal import MealSchema


meal_schema = MealSchema()
meals_schema = MealSchema(many=True)


class Meal(Resource):
    @classmethod
    @jwt_required()
    def get(cls, meal_id: int):
        meal = MealModel.find_by_id(meal_id)
        if not meal:
            return {'message': gettext('meal_not_found')}, 404
        return meal_schema.dump(meal), 200

    @classmethod
    @jwt_required()
    def post(cls):
        try:
            meal_data = request.get_json()
            user = UserModel.find_by_id(get_jwt_identity())
            meal = MealModel(user.id, date.today(), **meal_data)
            meal.save_to_db()
            return {'message': gettext('meal_created')}, 201
        except:
            traceback.print_exc()
            return {'message': gettext('meal_failed_to_create')}, 500

    @classmethod
    @jwt_required()
    def delete(cls, meal_id: int):
        meal = MealModel.find_by_id(meal_id)
        if not meal:
            return {'message': gettext('meal_not_found')}, 404
        meal.delete_from_db()
        return {'message': gettext('meal_deleted')}, 200


class DailyMeal(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        try:
            meal_date = request.args['date']
        except:
            return {'message': gettext('meal_invalid_date')}, 400
        user = UserModel.find_by_id(get_jwt_identity())
        meal_of_day = MealModel.find_meals_for_day(meal_date, user.id)
        return meal_schema.dump(meal_of_day)


class RemainingMeal(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        user = UserModel.find_by_id(get_jwt_identity())
        remaining = user.remaining_meal()
        return meal_schema.dump(remaining)


class AllMeals(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        user = UserModel.find_by_id(get_jwt_identity())
        meals = MealModel.find_by_user(user.id)
        return meals_schema.dump(meals)
