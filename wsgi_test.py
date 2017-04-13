import unittest
import json

import wsgi

API_URL = '/api/v1'


def extract_json(response):
    return json.loads(response.get_data())


class TestAPI(unittest.TestCase):
    def get_json(self, endpoint):
        return self.app.get(API_URL + str(endpoint), headers={'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsInV1aWQiOiI3N2JkN2M2My00YzIxLTRlYTktYmI2YS0yNTNlZDlhMjNlNTMifQ.zOBvRspbD2s-8aQVI0FtTG0mvR8W81NT0-ZdaMLLYvQ'})

    def post_json(self, endpoint, data):
        return self.app.post(API_URL + str(endpoint),
                             data=json.dumps(data),
                             content_type='application/json',
                             headers={'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsInV1aWQiOiI3N2JkN2M2My00YzIxLTRlYTktYmI2YS0yNTNlZDlhMjNlNTMifQ.zOBvRspbD2s-8aQVI0FtTG0mvR8W81NT0-ZdaMLLYvQ'})

    def setUp(self):
        self.app = wsgi.APP.test_client()

    def test1_get_orders(self):
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

    def test2_get_order(self):
        # TODO: (JWT) check response to unauthorized access

        # check response for nonexistent order
        response = self.get_json('/orders/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(extract_json(response), {
            'success': False,
            'message': 'NotFound'
        })

        # check response for existent order
        response = self.get_json('/orders/1')
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

    def test3_post_order(self):
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
