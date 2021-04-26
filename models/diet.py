from db import db


class DietModel(db.Model):

    __tablename__ = 'Diet'

    id = db.Column(db.Integer, primary_key=True)

    carbohydrate_portions = db.Column(db.Integer, nullable=False)
    fruit_portions = db.Column(db.Integer, nullable=False)
    vegetable_portions = db.Column(db.Integer, nullable=False)
    dairy_portions = db.Column(db.Integer, nullable=False)
    protein_portions = db.Column(db.Integer, nullable=False)
    polyunsaturated_fats_portions = db.Column(db.Integer, nullable=False)
    monounsaturated_fats_portions = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    user = db.relationship('UserModel', uselist=False)

    def __init__(self, user_id: int, carbohydrate_portions: int = 0,
                 fruit_portions: int = 0, vegetable_portions: int = 0,
                 dairy_portions: int = 0, protein_portions: int = 0,
                 polyunsaturated_fats_portions: int = 0,
                 monounsaturated_fats_portions: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.carbohydrate_portions = carbohydrate_portions
        self.fruit_portions = fruit_portions
        self.vegetable_portions = vegetable_portions
        self.dairy_portions = dairy_portions
        self.protein_portions = protein_portions
        self.polyunsaturated_fats_portions = polyunsaturated_fats_portions
        self.monounsaturated_fats_portions = monounsaturated_fats_portions

    @classmethod
    def find_by_id(cls, _id: int) -> "DietModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
