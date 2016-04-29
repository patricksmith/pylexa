from mock import patch
import unittest

from pylexa.intent import handle_intent


class TestHandleIntent(unittest.TestCase):

    def should_add_function_to_intents_dict(self):
        intents = {}
        with patch('pylexa.intent.intents', new=intents):
            @handle_intent('intent_name')
            def intent_handler(request):
                pass

        self.assertEqual(intents['intent_name'], intent_handler)
