# -*- coding: utf-8 -*-
from flask import Blueprint, request as flask_request

from pylexa.default_handlers import (
    default_launch_handler,
    default_session_ended_handler,
    default_unrecognized_intent_handler
)
from pylexa.intent import intents
from pylexa.request import IntentRequest, LaunchRequest, SessionEndedRequest, Request
from pylexa.response import PlainTextSpeech


alexa_blueprint = Blueprint('alexa', __name__)
alexa_blueprint.launch_handler = default_launch_handler
alexa_blueprint.session_ended_handler = default_session_ended_handler


def make_request_obj():
    type_ = flask_request.json.get('request', {}).get('type')
    request_classes = {
        'IntentRequest': IntentRequest,
        'LaunchRequest': LaunchRequest,
        'SessionEndedRequest': SessionEndedRequest
    }
    klass = request_classes.get(type_, Request)
    return klass(flask_request)


def handle_launch_request(func):
    alexa_blueprint.launch_handler = func
    return func


def handle_session_ended_request(func):
    alexa_blueprint.session_ended_handler = func
    return func


@alexa_blueprint.route('/', methods=['POST'])
def route_request():
    request = make_request_obj()
    if request.is_intent:
        if request.intent in intents:
            handler = intents[request.intent]
        else:
            handler = intents.get('unrecognized_intent', default_unrecognized_intent_handler)
        return handler(request)
    elif request.is_launch:
        return alexa_blueprint.launch_handler(request)
    elif request.is_session_ended:
        return alexa_blueprint.session_ended_handler(request)
    else:
        raise Exception('Invalid request type received')
