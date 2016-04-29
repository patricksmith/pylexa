from mock import Mock
import unittest

from pylexa.default_handlers import (
    default_launch_handler,
    default_session_ended_handler,
    default_unrecognized_intent_handler
)
from pylexa.response import PlainTextSpeech, Response


class TestDefaultLaunchHandler(unittest.TestCase):

    def should_return_launching_text(self):
        self.assertEqual(default_launch_handler(Mock()), PlainTextSpeech('Launching...'))


class TestDefaultSessionEndedHandler(unittest.TestCase):

    def should_return_emtpy_response(self):
        returned = default_session_ended_handler(Mock())
        self.assertIsInstance(returned, Response)
        self.assertEqual(returned.output_speech, {})


class TestDefaultUnrecognizedIntentHandler(unittest.TestCase):

    def should_return_speech(self):
        self.assertEqual(
            default_unrecognized_intent_handler(Mock()),
            PlainTextSpeech("I'm sorry, I didn't understand that")
        )

