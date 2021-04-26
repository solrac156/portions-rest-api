from ma import ma
from models.meal import MealModel


class MealSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MealModel
        dump_only = ('id',)
        load_only = ('user',)
        load_instance = True
        include_fk = True
