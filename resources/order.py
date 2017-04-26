from flask import current_app
from flask_restful import Resource, reqparse
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser, abort
import jwt

from models.order import OrderModel


def parse_jwt(authorization):
    # extract the JWT from the header
    token = authorization[7:]
    
    # decode the JWT with the shared secret
    # return None if the token was not valid
    try:
        return jwt.decode(token, current_app.config['SECRET_KEY'], audience='shop-example')
    except BaseException as e:
        print(str(e))
        return None

def extract_uuid(token):
    # extract the uuid from the sub claim
    return token['sub'][5:]


class OrderList(Resource):
    @use_kwargs({
        # get the auth header
        'authorization': fields.String(required=True, location='headers')
    })
    def get(self, authorization):
        # parse the token
        token = parse_jwt(authorization)
        if not token:
            return {
                'success': False,
                'messages': ['INVALID_TOKEN']
            }, 401

        # return the list of all items
        return {
            'success': True,
            'data': [order.to_json() for order in OrderModel.find_by_uuid(extract_uuid(token))]
        }

    @use_kwargs({
        # get the auth header
        'authorization': fields.String(required=True, location='headers'),
        # validate the array of products in the request
        'products': fields.List(fields.Nested({
            'quantity': fields.Int(required=True),
            'uuid': fields.Str(required=True)
        }), required=True, validate=lambda list: len(list) > 0)
    })
    def post(self, authorization, products):
        # parse the token
        token = parse_jwt(authorization)
        if not token:
            return {
                'success': False,
                'messages': ['INVALID_TOKEN']
            }, 401

        # construct a new order
        new_order = OrderModel(
            extract_uuid(token),
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
                'products': new_order.products 
            }
        }, 201


class Order(Resource):
    @use_kwargs({
        # get the auth header
        'authorization': fields.String(required=True, location='headers')
    })
    def get(self, authorization, id_):
        # parse the token
        token = parse_jwt(authorization)
        if not token:
            return {
                'success': False,
                'messages': ['INVALID_TOKEN']
            }, 401

        # get the order from the database
        item = OrderModel.find_by_id(id_)

        if item and item.user_uuid == extract_uuid(token):
            return {
                'success': True,
                'data': item.to_json()
            }

        # if the id doesn't exist, return 404
        # if the user is not permitted to access this order, return 404
        return {
            'success': False,
            'messages': ['NOT_FOUND']
        }, 404
