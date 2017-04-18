import unittest
import json
import jwt
import datetime
import wsgi


class TestAPI(unittest.TestCase):
    @staticmethod
    def extract_json(response):
        return json.loads(response.get_data())

    def get_json(self, endpoint, token=None):
        if not token:
            token = self.token

        # perform a GET request and attach the JWT
        return self.app.get(self.API_URL + str(endpoint),
                            headers={'Authorization': 'Bearer ' + str(token)})

    def post_json(self, endpoint, data, token=None):
        if not token:
            token = self.token

        # perform a POST request and attach the JWT
        return self.app.post(self.API_URL + str(endpoint),
                             data=json.dumps(data),
                             content_type='application/json',
                             headers={'Authorization': 'Bearer ' + str(token)})

    def setUp(self):
        self.app = wsgi.APP.test_client()
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiZTM1YjZhMGUtYjJiMS00YWZmLWFhMDgtYWFjZWY5YmQzMWE1IiwiZXhwIjo0MTAyNDQ0ODAwfQ.CR7RimGprQ21hROQZdMIiynny-aNSwVSfzPlyZeViLE'
        self.token_expired = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiZTM1YjZhMGUtYjJiMS00YWZmLWFhMDgtYWFjZWY5YmQzMWE1IiwiZXhwIjoxNDkyMDg5NjUxfQ.kpQF_Q8KzcLW73rgAOnuajLKGgKDz2rgvDtHruPNC_Q'
        self.token_invalid = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiZTM1YjZhMGUtYjJiMS00YWZmLWFhMDgtYWFjZWY5YmQzMWE1IiwiZXhwIjo0MTAyNDQ0ODAwfQ._lu0AlfzDqYn7E0ifZnFyiut0dIrssW3o6xnwf7-bg0'
        self.token_other = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiMDQyOWZhZDQtYTI3NS00ODgzLWFiNjItN2UyNWMyZTAwOGFhIiwiZXhwIjo0MTAyNDQ0ODAwfQ.yg4mH1NGIuby16KwCG-dvv0xnAR4t77A_zH1J7W75Iw'
        # TODO: dynamically generate a new token to be used in tests
        # self.token = jwt.encode(
        #    {'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        #     'uuid': '277323c8-cca8-410e-928a-88883a0983e1'},
        #    wsgi.APP.config['SECRET_KEY'])
        self.API_URL = '/api/v1'

    def test1_get_orders(self):
        # check response for empty list of orders
        response = self.get_json('/orders')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.extract_json(response), {
            'success': True,
            'data': []
        })

        # check response for non-empty list of orders
        response = self.post_json('/orders', {
            'products': [1, 2, 3]
        })
        response = self.get_json('/orders')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.extract_json(response), {
            'success': True,
            'data': [
                {
                    'fulfilled': False,
                    'id': 1,
                    'order_date': '01.01.1970',
                    'products': [1, 2, 3]
                }
            ]
        })

        # check response for invalid token
        for tk in [self.token_expired, self.token_invalid]:
            response = self.get_json('/orders', tk)
            self.assertEqual(response.status_code, 401)

    def test2_get_order(self):
        # check response for nonexistent order
        response = self.get_json('/orders/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.extract_json(response), {
            'success': False,
            'messages': ['NOT_FOUND']
        })

        # check response for existent order
        response = self.get_json('/orders/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.extract_json(response), {
            'success': True,
            'data': {
                'fulfilled': False,
                'id': 1,
                'order_date': '01.01.1970',
                'products': [1, 2, 3]
            }
        })

        # check response for invalid token
        for tk in [self.token_expired, self.token_invalid]:
            response = self.get_json('/orders/1', tk)
            self.assertEqual(response.status_code, 401)

        # check response if the order is not owned by requesting user
        response = self.get_json('/orders/1', self.token_other)
        self.assertEqual(response.status_code, 404)

    def test3_post_order(self):
        # check response for empty body
        response = self.post_json('/orders', {})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(self.extract_json(response), {
            'messages': {
                'products': ['Missing data for required field.']
            }
        })

        # check response for empty list of products
        response = self.post_json('/orders', {
            'products': []
        })
        self.assertEqual(response.status_code, 422)
        self.assertEqual(self.extract_json(response), {
            'messages': {
                'products': ['Invalid value.']
            }
        })

        # check response for valid body
        response = self.post_json('/orders', {
            'products': [1, 2, 3]
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.extract_json(response), {
            'success': True,
            'data': {
                'fulfilled': False,
                'id': 2,
                'products': [1, 2, 3]
            }
        })

        # check response for invalid token
        for tk in [self.token_expired, self.token_invalid]:
            response = self.post_json('/orders', {
                'products': [1]
            }, tk)
            self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
