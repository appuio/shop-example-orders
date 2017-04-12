import unittest
import json

from wsgi import APP, migrate

API_URL = '/api/v1'


def extract_json(response):
    return json.loads(response.get_data())


class TestAPI(unittest.TestCase):
    def get_json(self, endpoint):
        return self.app.get(API_URL + str(endpoint))

    def post_json(self, endpoint, data):
        return self.app.post(API_URL + str(endpoint),
                             data=json.dumps(data),
                             content_type='application/json')

    def setUp(self):
        migrate()
        self.app = APP.test_client()

    def test_get_orders(self):
        # check response for empty list of orders
        response = self.get_json('/orders')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(extract_json(response), {
            'success': True,
            'items': []
        })

        # check response for non-empty list of orders
        response = self.post_json('/orders', {
            'products': [1, 2, 3]
        })
        response = self.get_json('/orders')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(extract_json(response), {
            'success': True,
            'items': [
                {
                    'fulfilled': False,
                    'id': 1,
                    'order_date': '06.12.1993',
                    'products': [1, 2, 3]
                }
            ]
        })

    def test_get_order(self):
        # TODO: (JWT) check response to unauthorized access

        # check response for nonexistent order
        response = self.get_json('/orders/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(extract_json(response), {
            'success': False,
            'message': 'NotFound'
        })

        # check response for existent order
        repsonse = self.get_json('/orders/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(extract_json(response), {
            'success': True,
            'data': {
                'fulfilled': False,
                'id': 1,
                'order_date': '06.12.1993',
                'products': [1, 2, 3]
            }
        })

    def test_post_order(self):
        # TODO: (JWT) check response for unauthorized post

        # check response for empty body
        response = self.post_json('/orders', {})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(extract_json(response), {
            'messages': {
                'products': ['Missing data for required field.']
            }
        })

        # check response for empty list of products
        response = self.post_json('/orders', {
            'products': []
        })
        self.assertEqual(response.status_code, 422)
        self.assertEqual(extract_json(response), {
            'messages': {
                'products': ['Invalid value.']
            }
        })

        # check response for valid body
        response = self.post_json('/orders', {
            'products': [1, 2, 3]
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(extract_json(response), {
            'success': True,
            'data': {
                'fulfilled': False,
                'id': 2,
                'products': [1, 2, 3]
            }
        })


if __name__ == '__main__':
    unittest.main()
