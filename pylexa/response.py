# -*- coding: utf-8 -*-
from flask import Response as BaseResponse, jsonify


class AlexaResponseWrapper(BaseResponse):

    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, OutputSpeech):
            rv = Response(speech=rv)
        if isinstance(rv, Response):
            rv = jsonify(rv.as_dict())
        return super(AlexaResponseWrapper, cls).force_type(rv, environ)


class Card(object):

    type_ = None

    def as_dict(self):
        return dict(
            type=self.type_,
            **self.get_properties()
        )

    def get_properties(self):
        return {}


class SimpleCard(Card):

    type_ = 'Simple'

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def get_properties(self):
        return {
            'title': self.title,
            'content': self.content
        }


class StandardCard(Card):

    type_ = 'Standard'

    def __init__(self, title, text, smallImage, largeImage):
        self.title = title
        self.text = text
        self.smallImage = smallImage
        self.largeImage = largeImage

    def get_properties(self):
        return {
            'title': self.title,
            'text': self.text,
            'image': {
                'smallImageUrl': self.smallImage,
                'largeImageUrl': self.largeImage
            }
        }


class LinkAccountCard(Card):

    type_ = 'LinkAccount'

    def __init__(self):
        pass


class OutputSpeech(object):

    type_ = None

    def get_properties(self):
        return {}

    def as_dict(self):
        return dict(
            type=self.type_,
            **self.get_properties()
        )

    def __eq__(self, other):
        return (
            self.type_ == other.type_ and
            self.get_properties() == other.get_properties()
        )


class PlainTextSpeech(OutputSpeech):

    type_ = 'PlainText'

    def __init__(self, text):
        self.text = text

    def get_properties(self):
        return { 'text': self.text }


class SSMLSpeech(OutputSpeech):

    type_ = 'SSML'

    def __init__(self, ssml):
        self.ssml = ssml

    def get_properties(self):
        return { 'ssml': self.ssml }


class Response(object):

    version = '1.0'
    output_speech = {}

    def __init__(self, speech=None, card=None, reprompt=None, session=None, should_end_session=True):
        self.speech = speech
        self.card = card
        self.reprompt = reprompt
        self.session = session
        self.should_end_session = should_end_session

    def as_dict(self):
        response = {
            'shouldEndSession': self.should_end_session,
        }
        if self.speech:
            response['outputSpeech'] = self.speech.as_dict()
        if self.card:
            response['card'] = self.card.as_dict()
        if self.reprompt:
            response['reprompt'] = {
                'outputSpeech': self.reprompt.as_dict()
            }

        return {
            'version': self.version,
            'response': response,
            'sessionAttributes': self.session,
        }
