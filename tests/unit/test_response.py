import unittest

from pylexa.response import (
    LinkAccountCard,
    PlainTextSpeech,
    Response,
    SimpleCard,
    SSMLSpeech,
    StandardCard,
)


class TestSimpleCard(unittest.TestCase):

    def should_return_title_and_content_in_dict(self):
        title = 'title'
        content = 'content'
        card = SimpleCard(title, content)
        self.assertEqual(card.as_dict(), {
            'type': 'Simple',
            'title': title,
            'content': content
        })


class TestStandardCard(unittest.TestCase):

    def should_return_standard_card_dict(self):
        title = 'title'
        text = 'text'
        smallImageUrl = 'http://small.image.url'
        largeImageUrl = 'http://large.image.url'

        card = StandardCard(title, text, smallImageUrl, largeImageUrl)

        self.assertEqual(card.as_dict(), {
            'type': 'Standard',
            'title': title,
            'text': text,
            'image': {
                'smallImageUrl': smallImageUrl,
                'largeImageUrl': largeImageUrl
            }
        })


class TestLinkAccountCard(unittest.TestCase):

    def should_return_link_account_card(self):
        card = LinkAccountCard()
        self.assertEqual(card.as_dict(), {'type': 'LinkAccount'})


class TestPlainTextSpeech(unittest.TestCase):

    def should_return_text_in_dict(self):
        text = 'This is some text'
        speech = PlainTextSpeech(text)
        self.assertEqual(speech.as_dict(), {
            'type': 'PlainText',
            'text': text
        })


class TestSSMLSpeech(unittest.TestCase):

    def should_return_ssml_in_dict(self):
        ssml = 'Here is a word spelled out: <say-as interpret-as="spell-out">hello</say-as>'
        speech = SSMLSpeech(ssml)
        self.assertEqual(speech.as_dict(), {
            'type': 'SSML',
            'ssml': ssml
        })


class _BaseResponseTestCase(unittest.TestCase):

    speech = None
    card = None
    should_end_session = True

    def should_return_expected_dict(self):
        response = Response(self.speech, self.card, self.should_end_session)
        self.assertEqual(response.as_dict(), self.expected_output)


class TestDefaultResponse(_BaseResponseTestCase):

    expected_output = {
        'version': '1.0',
        'response': {
            'shouldEndSession': True
        }
    }

class TestResponseWithSpeech(_BaseResponseTestCase):

    speech = PlainTextSpeech('This is some text')
    expected_output = {
        'version': '1.0',
        'response': {
            'shouldEndSession': True,
            'outputSpeech': {
                'type': 'PlainText',
                'text': 'This is some text'
            }
        }
    }


class TestResponseWithCard(_BaseResponseTestCase):

    card = SimpleCard('Card title', 'Card content')
    expected_output = {
        'version': '1.0',
        'response': {
            'shouldEndSession': True,
            'card': {
                'type': 'Simple',
                'title': 'Card title',
                'content': 'Card content'
            }
        }
    }


class TestResponseWithSpeechAndCard(_BaseResponseTestCase):

    speech = PlainTextSpeech('This is some text')
    card = SimpleCard('Card title', 'Card content')
    expected_output = {
        'version': '1.0',
        'response': {
            'shouldEndSession': True,
            'card': {
                'type': 'Simple',
                'title': 'Card title',
                'content': 'Card content',
            }, 'outputSpeech': {
                'type': 'PlainText',
                'text': 'This is some text'
            }
        }
    }


class TestResponseWithShouldEndSession(_BaseResponseTestCase):

    should_end_session = False
    expected_output = {
        'version': '1.0',
        'response': {
            'shouldEndSession': False
        }
    }
