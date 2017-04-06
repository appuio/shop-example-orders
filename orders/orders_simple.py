import os as os
from flask import Flask, jsonify, request

# create the application instance
APP = Flask(__name__)

# load the configuration from the environment
APP.config.update(
    DB_HOSTNAME=os.environ['DB_HOSTNAME'],
    DB_USERNAME=os.environ['DB_USERNAME'],
    DB_PASSWORD=os.environ['DB_PASSWORD'],
    DB_DATABASE=os.environ['DB_DATABASE']
)

@APP.route('/api/v1/orders', methods=['GET'])
def get_orders():
    # TODO: validate the JWT
    # TODO: get the UUID from the JWT
    # TODO: lookup all orders corresponding to the JWT

    # return appropriate response
    return jsonify({
        'success': True,
        'items': [
            {'id': 1}
        ]
    })

# place a new order using POST
@APP.route('/api/v1/orders', methods=['POST'])
def place_order():
    # TODO: validate the JWT
    # TODO: get the UUID from the JWT

    # TODO: add the order to the database
    ## get the request body
    body = request.get_json()

    # return appropriate response
    return jsonify({
        'success': True,
        'data': {
            'id': 1
        }
    })

# get order details using GET
@APP.route('/api/v1/orders/<int:order_id>')
def get_order(order_id):
    # TODO: validate the JWT
    # TODO: get the UUID from the JWT
    # TODO: get the order from the database
    # TODO: verify that the UUID matches the order

    # return appropriate response
    return jsonify({
        'success': True,
        'data': {
            'id': order_id
        }
    })
