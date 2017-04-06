import os as os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# create the application instance
APP = Flask(__name__)

# load the configuration from the environment
APP.config.update(
    DB_HOSTNAME=os.environ['DB_HOSTNAME'],
    DB_USERNAME=os.environ['DB_USERNAME'],
    DB_PASSWORD=os.environ['DB_PASSWORD'],
    DB_DATABASE=os.environ['DB_DATABASE']
)

# place a new order using POST
@APP.route('/api/v1/orders', methods=['POST'])
def orders():
    return 'TODO: orders'

# get order details using GET
@APP.route('/api/v1/orders/<int:order_id>')
def order(order_id):
    return 'TODO: order ' + str(order_id)
