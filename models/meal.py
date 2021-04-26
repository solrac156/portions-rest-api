from typing import List

from dateutil.parser import parse

from db import db
from datetime import date


class MealModel(db.Model):

    __tablename__ = 'Meal'

    id = db.Column(db.Integer, primary_key=True)
    meal_date = db.Column(db.Date, nullable=False)
    carbohydrate_portions = db.Column(db.Integer)
    fruit_portions = db.Column(db.Integer)
    vegetable_portions = db.Column(db.Integer)
    dairy_portions = db.Column(db.Integer)
    protein_portions = db.Column(db.Integer)
    polyunsaturated_fats_portions = db.Column(db.Integer)
    monounsaturated_fats_portions = db.Column(db.Integer)
    description = db.Column(db.String(80))

    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    user = db.relationship('UserModel')

    def __init__(self, user_id: int, meal_date: date,
                 carbohydrate_portions: int = 0, fruit_portions: int = 0,
                 vegetable_portions: int = 0, dairy_portions: int = 0,
                 protein_portions: int = 0,
                 polyunsaturated_fats_portions: int = 0,
                 monounsaturated_fats_portions: int = 0, description: str = '',
                 **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.meal_date = meal_date
        self.carbohydrate_portions = carbohydrate_portions
        self.fruit_portions = fruit_portions
        self.vegetable_portions = vegetable_portions
        self.dairy_portions = dairy_portions
        self.protein_portions = protein_portions
        self.polyunsaturated_fats_portions = polyunsaturated_fats_portions
        self.monounsaturated_fats_portions = monounsaturated_fats_portions
        self.description = description

    @classmethod
    def find_by_id(cls, _id: int) -> "MealModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_meals_for_day(cls, meal_date: str, user_id: int) -> "MealModel":
        meals = cls.query.filter_by(meal_date=meal_date, user_id=user_id).all()
        meal_values = dict()
        meal_values['carbohydrate_portions'] = 0
        meal_values['fruit_portions'] = 0
        meal_values['vegetable_portions'] = 0
        meal_values['dairy_portions'] = 0
        meal_values['protein_portions'] = 0
        meal_values['polyunsaturated_fats_portions'] = 0
        meal_values['monounsaturated_fats_portions'] = 0
        for meal in meals:
            meal_values['carbohydrate_portions'] += meal.carbohydrate_portions
            meal_values['fruit_portions'] += meal.fruit_portions
            meal_values['vegetable_portions'] += meal.vegetable_portions
            meal_values['dairy_portions'] += meal.dairy_portions
            meal_values['protein_portions'] += meal.protein_portions
            meal_values['polyunsaturated_fats_portions'] += \
                meal.polyunsaturated_fats_portions
            meal_values['monounsaturated_fats_portions'] += \
                meal.monounsaturated_fats_portions
        meal_values['meal_date'] = parse(meal_date).date()
        meal_values['description'] = f'Total portions eaten on {meal_date}.'
        meal_values['user_id'] = user_id
        meal_of_the_day = cls(**meal_values)
        return meal_of_the_day

    @classmethod
    def find_by_user(cls, user_id: int) -> List["MealModel"]:
        return cls.query.filter_by(user_id=user_id).all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
