import json
import unittest

from tests.integration.app_for_testing import app


EXAMPLE_REQUEST = {
    'request': {
        'locale': 'en-US',
        'requestId': 'EdwRequestId',
        'timestamp': '2016-04-19T14:28:53Z',
        'type': 'IntentRequest'
    },
    'session': {
        'application': {
            'applicationId': 'amzn1.echo-sdk-ams.app.app_id'
        },
        'new': True,
        'sessionId': 'SessionId.session_id',
        'user': {
            'userId': 'amzn1.ask.account.user_id'
        }
    },
    'version': '1.0'
}


class TestInvalidRequest(unittest.TestCase):

    def setUp(self):
        self.old_app_debug = app.debug
        app.debug = False

    def tearDown(self):
        app.debug = self.old_app_debug

    def should_return_400_status_code(self):
        with app.test_client() as client:
            rv = client.post(
                '/',
                data=json.dumps(EXAMPLE_REQUEST),
                headers={'content-type': 'application/json'}
            )
        self.assertEqual(rv.status_code, 400)


class TestRequestForDifferentApplication(unittest.TestCase):

    def setUp(self):
        self.blueprint = app.blueprints['alexa']
        self.old_app_id = app.config.get('app_id')
        app.config['app_id'] = 'incorrect_app_id'

    def tearDown(self):
        app.config['app_id'] = self.old_app_id

    def should_return_400_status_code(self):
        with app.test_client() as client:
            rv = client.post(
                '/',
                data=json.dumps(EXAMPLE_REQUEST),
                headers={'content-type': 'application/json'}
            )
        self.assertEqual(rv.status_code, 400)
