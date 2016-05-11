import json
import unittest

from app_for_testing import app


app.debug = True


EXAMPLE_REQUEST = {
    'request': {
        'locale': 'en-US',
        'requestId': 'EdwRequestId',
        'timestamp': '2016-04-19T14:28:53Z',
        'type': 'SessionEndedRequest'
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


class TestSessionEndedRequest(unittest.TestCase):

    def should_return_speech_response(self):
        with app.test_client() as client:
            rv = client.post(
                '/',
                data=json.dumps(EXAMPLE_REQUEST),
                headers={'content-type': 'application/json'}
            )
            self.assertEqual(json.loads(rv.get_data()), {
                'version': '1.0',
                'response': {
                    'outputSpeech': {
                        'type': 'PlainText',
                        'text': 'Later, alligator'
                    },
                    'shouldEndSession': True
                },
                'sessionAttributes': None,
            })


