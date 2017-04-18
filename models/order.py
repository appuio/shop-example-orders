from sqlalchemy.dialects import postgresql

from db import db


class OrderModel(db.Model):
    # define the database table sqlalchemy should use
    __tablename__ = 'orders'

    # define the structure of the database table
    id = db.Column(db.Integer, primary_key=True)
    user_uuid = db.Column(postgresql.UUID)
    products = db.Column(postgresql.ARRAY(db.Integer, dimensions=1))
    order_date = db.Column(db.DateTime)
    fulfilled = db.Column(db.Boolean)

    def __init__(self, user_uuid, products, order_date, fulfilled):
        self.user_uuid = user_uuid
        self.products = products
        self.order_date = order_date
        self.fulfilled = fulfilled

    @classmethod
    def find_by_id(cls, id_):
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(user_uuid=uuid).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {
            'id'        : self.id,
            'products'  : self.products,
            'order_date': '01.01.1970',  # TODO: return a serialized date
            'fulfilled' : self.fulfilled
        }
