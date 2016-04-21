# -*- coding: utf-8 -*-
from flask import Blueprint, request as flask_request

from pylexa.intent import intents
from pylexa.request import IntentRequest, LaunchRequest, SessionEndedRequest, Request
from pylexa.response import PlainTextSpeech


alexa_blueprint = Blueprint('alexa', __name__)


def make_request_obj(flask_request):
    type_ = flask_request.json.get('request', {}).get('type')
    request_classes = {
        'IntentRequest': IntentRequest,
        'LaunchRequest': LaunchRequest,
        'SessionEndedRequest': SessionEndedRequest
    }
    klass = request_classes.get(type_, Request)
    return klass(flask_request)


@alexa_blueprint.route('/', methods=['POST'])
def handle_request():
    print flask_request.json
    request = make_request_obj(flask_request)
    if request.is_intent:
        if request.intent in intents:
            return intents[request.intent](request)
        else:
            return PlainTextSpeech("I'm sorry I didn't understand that")
    elif request.is_launch:
        return PlainTextSpeech('Launching')
    else:
        return PlainTextSpeech('¯\_(ツ)_/¯')
