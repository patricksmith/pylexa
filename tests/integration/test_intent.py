import json
import unittest

from app_for_testing import app


def make_echo_request(slot_value=None):
    slot = {
        'name': 'message'
    }
    if slot_value:
        slot['value'] = slot_value

    return {
        'request': {
            'locale': 'en-US',
            'requestId': 'EdwRequestId',
            'timestamp': '2016-04-19T14:28:53Z',
            'type': 'IntentRequest',
            'intent': {
                'name': 'Echo',
                'slots': {
                    'message': slot
                }
            }
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


class TestEchoIntentWithoutValue(unittest.TestCase):

    def should_return_nothing_to_echo_speech(self):
        with app.test_client() as client:
            rv = client.post(
                '/',
                data=json.dumps(make_echo_request()),
                headers={'content-type': 'application/json'}
            )
            self.assertEqual(json.loads(rv.get_data()), {
                'version': '1.0',
                'response': {
                    'outputSpeech': {
                        'type': 'PlainText',
                        'text': 'Nothing to echo'
                    },
                    'shouldEndSession': True
                },
                'sessionAttributes': None,
            })


class TestEchoIntentWithValue(unittest.TestCase):

    def should_return_nothing_to_echo_speech(self):
        with app.test_client() as client:
            rv = client.post(
                '/',
                data=json.dumps(make_echo_request('echo me')),
                headers={'content-type': 'application/json'}
            )
            self.assertEqual(json.loads(rv.get_data()), {
                'version': '1.0',
                'response': {
                    'outputSpeech': {
                        'type': 'PlainText',
                        'text': 'echo me'
                    },
                    'shouldEndSession': True
                },
                'sessionAttributes': None,
            })


EXAMPLE_REQUIRES_AUTH_REQUEST = {
    'request': {
        'locale': 'en-US',
        'requestId': 'EdwRequestId',
        'timestamp': '2016-04-19T14:28:53Z',
        'type': 'IntentRequest',
        'intent': {
            'name': 'RequiresAuth',
            'slots': {}
        }
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


class TestAuthIntent(unittest.TestCase):

    def should_return_card_with_speech(self):
        with app.test_client() as client:
            rv = client.post(
                '/',
                data=json.dumps(EXAMPLE_REQUIRES_AUTH_REQUEST),
                headers={'content-type': 'application/json'}
            )
            self.assertEqual(json.loads(rv.get_data()), {
                'version': '1.0',
                'response': {
                    'outputSpeech': {
                        'type': 'PlainText',
                        'text': 'You need to link your account first'
                    },
                    'card': {
                        'type': 'LinkAccount'
                    },
                    'shouldEndSession': True
                },
                'sessionAttributes': None,
            })
