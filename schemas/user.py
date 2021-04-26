from ma import ma
from models.user import UserModel
from schemas.diet import DietSchema


class UserSchema(ma.SQLAlchemyAutoSchema):

    diet = ma.Nested(DietSchema)

    class Meta:
        model = UserModel
        load_only = ('password',)
        dump_only = ('id',)
        load_instance = True
        include_fk = True
