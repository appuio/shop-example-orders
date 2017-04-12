import os as os

from flask import Flask
from flask_restful import Api
from sqlalchemy.engine.url import URL

from resources.order import Order, OrderList

# read database settings from the environment
DB_SETTINGS = {
    'drivername': 'postgresql',
    'host': os.environ.get('DB_HOSTNAME', '172.28.128.3'),
    'port': 5432,
    'username': os.environ.get('DB_USERNAME', 'orders'),
    'password': os.environ.get('DB_PASSWORD', 'secret'),
    'database': os.environ.get('DB_DATABASE', 'orders')
}

# initialize the APP
APP = Flask(__name__)
APP.secret_key = os.environ.get('SECRET_KEY', 'abcd')
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['SQLALCHEMY_DATABASE_URI'] = URL(**DB_SETTINGS)

# initialize the API
API = Api(APP)
API.add_resource(OrderList, '/api/v1/orders')
API.add_resource(Order, '/api/v1/orders/<int:id_>')


@APP.before_first_request
def migrate():
    from db import db

    # initialize the database with the necessary tables
    db.create_all()


# prepare the application for testing / running
@APP.before_request
def prepare():
    from db import db

    # initialize the database connection
    db.init_app(APP)


# destroy the database connection
@APP.teardown_request
def teardown(exception):
    db.close()


if __name__ == '__main__':
    APP.run(port=os.environ.get('PORT', 5000),
            debug=os.environ.get('DEBUG', True))
