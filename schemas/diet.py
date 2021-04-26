from ma import ma
from models.diet import DietModel


class DietSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DietModel
        load_only = ('user',)
        dump_only = ('id',)
        load_instance = True
        include_fk = True
