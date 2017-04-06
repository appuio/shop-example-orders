from flask import Flask, request
from flask_restful import Resource, Api, reqparse

APP = Flask(__name__)
API = Api(APP)

items = []


class OrderList(Resource):
    def get(self):
        # TODO: validate the JWT
        # TODO: get the UUID from the JWT
        # TODO: lookup all orders corresponding to the JWT

        # return the list of all items
        return {
            'success': True,
            'items': items
        }

    def post(self):
        # set up input validation
        parser = reqparse.RequestParser()
        parser.add_argument('uuid',
                            type=str,
                            required=True)
        parser.add_argument('products',
                            type=list,
                            required=True,
                            location='json') # type='list' -> location='json'

        # read the request body with reqparse
        data = parser.parse_args()

        # parse the request body to json
        # silent=True => return None if invalid
        # data = request.get_json(silent=True)

        # check whether the body was valid json
        if data is not None:
            items.append(data)

            # TODO: validate the JWT
            # TODO: get the UUID from the JWT
            # TODO: add the order to the database
            return {
                'success': True,
                'data': data
            }, 201

        # return "bad request"
        return {
            'success': False,
            'message': 'INVALID_BODY'
        }, 400


class Order(Resource):
    def get(self, id):
        # TODO: validate the JWT
        # TODO: get the UUID from the JWT
        # TODO: get the order from the database
        # TODO: verify that the UUID matches the order

        # use next to get the first item returned by the filter
        # specify None as a default value for the next function
        item = next(filter(lambda x: x['id'] == id, items), None)

        if item is not None:
            return {
                'success': True,
                'data': {
                    'id': id
                }
            }

        # if the id doesn't exist, return 404
        return {
            'success': False,
            'message': 'NotFound'
        }, 404


API.add_resource(OrderList, '/api/v1/orders')
API.add_resource(Order, '/api/v1/orders/<int:id>')
