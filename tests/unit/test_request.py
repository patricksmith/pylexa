from mock import Mock
import unittest

from pylexa.request import Request, LaunchRequest, IntentRequest, SessionEndedRequest



class TestRequestClass(unittest.TestCase):

    def setUp(self):
        self.access_token = 'DEADBEEF'
        self.request_type = 'request_type'
        self.timestamp = '2016-04-14T19:31:51Z'
        self.request_id = 'EdwRequestId.REQUEST_ID'

        incoming_request = Mock(json={
            'request': {
                'type': self.request_type,
                'requestId': self.request_id,
                'timestamp': self.timestamp,
            }, 'session': {
                'user': {
                    'accessToken': self.access_token,
                },
                'attributes': None
            },
        })

        self.request = Request(incoming_request)

    def should_return_request_type(self):
        self.assertEqual(self.request.type, self.request_type)

    def should_return_timestamp(self):
        self.assertEqual(self.request.timestamp, self.timestamp)

    def should_return_request_id(self):
        self.assertEqual(self.request.request_id, self.request_id)

    def should_return_access_token(self):
        self.assertEqual(self.request.access_token, self.access_token)

    def should_not_set_request_type_booleans(self):
        self.assertFalse(self.request.is_intent)
        self.assertFalse(self.request.is_launch)
        self.assertFalse(self.request.is_session_ended)

    def should_return_emtpy_dict_for_session(self):
        self.assertEqual(self.request.session, {})


class TestLaunchRequest(unittest.TestCase):

    def should_set_is_launch(self):
        self.assertTrue(LaunchRequest(Mock()).is_launch)


class TestIntentRequest(unittest.TestCase):

    def setUp(self):
        incoming_request = Mock(json={
            'request': {
                'intent': {
                    'name': 'intent_name',
                    'slots': {
                        'slot_with_value': {
                            'name': 'slot_with_value',
                            'value': 'value'
                        },
                        'slot_without_value': {
                            'name': 'slot_without_value',
                        },
                    }
                },
            },
        })

        self.request = IntentRequest(incoming_request)

    def should_set_is_intent(self):
        self.assertTrue(self.request.is_intent)

    def should_return_intent_name(self):
        self.assertEqual(self.request.intent, 'intent_name')

    def should_return_slots_with_values(self):
        self.assertEqual(self.request.slots, {'slot_with_value': 'value'})


class TestSessionEndedRequest(unittest.TestCase):

    def setUp(self):
        incoming_request = Mock(json={
            'request': {
                'reason': 'reason for ending session'
            }
        })
        self.request = SessionEndedRequest(incoming_request)

    def should_set_is_session_ended(self):
        self.assertTrue(self.request.is_session_ended)

    def should_return_reason(self):
        self.assertEqual(self.request.reason, 'reason for ending session')
