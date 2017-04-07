import os as os

from flask import Flask
from flask_restful import Api
from sqlalchemy.engine.url import URL

from resources.order import Order, OrderList

DB_SETTINGS = {
    'drivername': 'postgres',
    'host'      : os.environ['DB_HOSTNAME'],
    'port'      : 5432,
    'username'  : os.environ['DB_USERNAME'],
    'password'  : os.environ['DB_PASSWORD'],
    'database'  : os.environ['DB_DATABASE']
}

APP = Flask(__name__)
APP.secret_key = 'acbd'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['SQLALCHEMY_DATABASE_URI'] = URL(**DB_SETTINGS)

API = Api(APP)

API.add_resource(OrderList, '/api/v1/orders')
API.add_resource(Order, '/api/v1/orders/<int:id_>')

if __name__ == '__main__':
    from db import db

    db.init_app(APP)
    APP.run(port=5000, debug=True)
