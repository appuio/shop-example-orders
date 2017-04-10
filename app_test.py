import unittest
import json
# import tempfile

import app


class TestAPI(unittest.TestCase):
    def setUp(self):
        # self.tmp_db, self.tmp_db_path = tempfile.mkstemp()
        # app.APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://scott:tiger@localhost/mydatabase' + self.tmp_db_path
        app.prepare()
        self.app = app.APP.test_client()

    def tearDown(self):
        # TODO: reset the database?
        pass

    def test_get_orders(self):
        # check response for empty list of orders
        response = self.app.get('/api/v1/orders')
        self.assertEqual(json.loads(response.get_data()), {
            'success': True,
            'items': []
        })

        # TODO: check response for non-empty list of orders

    def test_get_order(self):
        # check response for nonexistent order
        response = self.app.get('/api/v1/orders/99')
        self.assertEqual(json.loads(response.get_data()), {
            'success': False,
            'message': 'NotFound'
        })

        # add a first order to the database
        response = self.app.post('/api/v1/orders', data={
            'uuid': 'abcd',
            'products': [1, 2, 3]
        })
        self.assertEqual(json.loads(response.get_data()), {})

        # TODO: (JWT) check response to unauthorized access

    def test_post_order(self):
        # TODO: check response for empty body
        # TODO: check response for incomplete body
        # TODO: check response for valid body
        # TODO: (JWT) check response for unauthorized post
        pass

if __name__ == '__main__':
    unittest.main()
