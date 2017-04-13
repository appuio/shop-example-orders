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
APP.secret_key = os.environ.get('SECRET_KEY', 'secret')
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['SQLALCHEMY_DATABASE_URI'] = URL(**DB_SETTINGS)

# initialize the API
API = Api(APP)
API.add_resource(OrderList, '/api/v1/orders')
API.add_resource(Order, '/api/v1/orders/<int:id_>')

# initialize the database before the first request is served
@APP.before_first_request
def migrate():
    from db import db

    db.init_app(APP)

    # setup the necessary tables (very simple "migration")
    db.create_all()


if __name__ == '__main__':
    APP.run(port=os.environ.get('PORT', 5000),
            debug=os.environ.get('DEBUG', True))
