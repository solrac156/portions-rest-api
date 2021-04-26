from dateutil.parser import parse
from dateutil.utils import today

from db import db
from models.meal import MealModel


class UserModel(db.Model):

    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    diet = db.relationship('DietModel', uselist=False)
    meals = db.relationship('MealModel', lazy='dynamic')

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    def remaining_meal(self, date: str = None) -> "MealModel":
        if not date:
            date = parse(str(today())).date()
        user_diet = self.diet
        day_meal = MealModel.find_meals_for_day(str(date), self.id)
        meal_values = dict()
        meal_values['carbohydrate_portions'] = \
            user_diet.carbohydrate_portions - day_meal.carbohydrate_portions
        meal_values['fruit_portions'] = \
            user_diet.fruit_portions - day_meal.fruit_portions
        meal_values['vegetable_portions'] = \
            user_diet.vegetable_portions - day_meal.vegetable_portions
        meal_values['dairy_portions'] = \
            user_diet.dairy_portions - day_meal.dairy_portions
        meal_values['protein_portions'] = \
            user_diet.protein_portions - day_meal.protein_portions
        meal_values['polyunsaturated_fats_portions'] = \
            user_diet.polyunsaturated_fats_portions - \
            day_meal.polyunsaturated_fats_portions
        meal_values['monounsaturated_fats_portions'] = \
            user_diet.monounsaturated_fats_portions - \
            day_meal.monounsaturated_fats_portions
        meal_values['meal_date'] = date
        meal_values['user_id'] = self.id
        meal_values['description'] = f'Remaining portions for {date}'
        return MealModel(**meal_values)

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
