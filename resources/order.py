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
        return jwt.decode(token, current_app.config['SECRET_KEY'])
    except Exception:
        return None


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
                'message': 'INVALID_TOKEN'
            }, 401

        # return the list of all items
        return {
            'success': True,
            'items': [order.to_json() for order in OrderModel.find_by_uuid(token['uuid'])]
        }

    @use_kwargs({
        # get the auth header
        'authorization': fields.String(required=True, location='headers'),
        # validate the array of products in the request
        'products': fields.List(fields.Int(), required=True, validate=lambda list: len(list) > 0)
    })
    def post(self, authorization, products):
        # parse the token
        token = parse_jwt(authorization)
        if not token:
            return {
                'success': False,
                'message': 'INVALID_TOKEN'
            }, 401

        # construct a new order
        new_order = OrderModel(
            token['uuid'],
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
                'message': 'INVALID_TOKEN'
            }, 401

        # get the order from the database
        item = OrderModel.find_by_id(id_)

        if item and item.user_uuid == token['uuid']:
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
