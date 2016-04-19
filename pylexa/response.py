from flask import Response as BaseResponse, jsonify


class AlexaResponse(BaseResponse):

    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, Response):
            rv = jsonify(rv.as_dict())
        return super(AlexaResponse, cls).force_type(rv, environ)


class Response(object):

    version = '1.0'
    output_speech = {}

    def __init__(self, should_end_session=False):
        self.should_end_session = should_end_session

    def as_dict(self):
        return {
            'version': self.version,
            'response': {
                'shouldEndSession': self.should_end_session,
                'outputSpeech': self.output_speech
            }
        }


class PlainTextResponse(Response):

    def __init__(self, text, *args, **kwargs):
        self.output_speech = {
            'type': 'PlainText',
            'text': text
        }
        super(PlainTextResponse, self).__init__(*args, **kwargs)
