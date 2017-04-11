from flask_restful import Resource, reqparse
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser, abort

from models.order import OrderModel


class OrderList(Resource):
    def get(self):
        # TODO: validate the JWT
        # TODO: get the UUID from the JWT
        uuid = '77bd7c63-4c21-4ea9-bb6a-253ed9a23e53'

        # return the list of all items
        return {
            'success': True,
            'items': [order.to_json() for order in OrderModel.find_by_uuid(uuid)]
        }

    @use_kwargs({
        # validate the array of products in the request
        'products': fields.List(fields.Int(), required=True, validate=lambda list: len(list) > 0)
    })
    def post(self, products):
        # TODO: validate the JWT
        # TODO: get the UUID from the JWT
        uuid = '77bd7c63-4c21-4ea9-bb6a-253ed9a23e53'

        # construct a new order
        new_order = OrderModel(
            uuid,
            products,
            '2017-10-10 20:00:00',
            False
        )

        # add the order to the database
        OrderModel.save_to_db(new_order)

        return {
            'success': True,
            'data': {
                'fulfilled': new_order.fulfilled,
                'id': new_order.id,
                'products': products
            }
        }, 201


class Order(Resource):
    def get(self, id_):
        # TODO: validate the JWT
        # TODO: get the UUID from the JWT
        uuid = '77bd7c63-4c21-4ea9-bb6a-253ed9a23e53'

        # get the order from the database
        item = OrderModel.find_by_id(id_)

        if item and item.user_uuid == uuid:
            return {
                'success': True,
                'data': item.to_json()
            }

        # if the id doesn't exist, return 404
        # if the user is not permitted to access this order, return 404
        return {
            'success': False,
            'message': 'NotFound'
        }, 404
