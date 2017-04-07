from flask_restful import Resource, reqparse

from models.order import OrderModel


class OrderList(Resource):
    def get(self):
        # TODO: validate the JWT
        # TODO: get the UUID from the JWT
        uuid = '77bd7c63-4c21-4ea9-bb6a-253ed9a23e53'

        # return the list of all items
        return {
            'success': True,
            'items'  : [order.to_json() for order in OrderModel.find_by_uuid(uuid)]
        }

    def post(self):
        # TODO: validate the JWT
        # TODO: get the UUID from the JWT
        uuid = '77bd7c63-4c21-4ea9-bb6a-253ed9a23e53'

        # set up input validation
        # the only data we expect is a list of products for the order
        parser = reqparse.RequestParser()
        parser.add_argument('products',
                            type=list,
                            required=True,
                            location='json')  # type='list' only works with location='json'

        # read the request body with reqparse
        data = parser.parse_args()

        # parse the request body to json
        # silent=True => return None if invalid
        # data = request.get_json(silent=True)

        # check whether the body was valid json
        if data:
            # add the order to the database
            OrderModel.save_to_db(OrderModel(
                uuid,
                data.products,
                '2017-10-10 20:00:00',
                False
            ))

            return {
                       'success': True,
                       'data'   : {}  # return some data?
                   }, 201

        # return "bad request"
        return {
                   'success': False,
                   'message': 'INVALID_BODY'
               }, 400


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
                'data'   : item.to_json()
            }

        # if the id doesn't exist, return 404
        # if the user is not permitted to access this order, return 404
        return {
                   'success': False,
                   'message': 'NotFound'
               }, 404
