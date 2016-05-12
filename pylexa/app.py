# -*- coding: utf-8 -*-
from flask import Blueprint, current_app, jsonify, request as flask_request

from pylexa.default_handlers import (
    default_launch_handler,
    default_session_ended_handler,
    default_unrecognized_intent_handler
)
from pylexa.exceptions import InvalidRequest
from pylexa.intent import intents
from pylexa.request import IntentRequest, LaunchRequest, SessionEndedRequest, Request
from pylexa.response import PlainTextSpeech
from pylexa.verify import verify_request


alexa_blueprint = Blueprint('alexa', __name__)
alexa_blueprint.launch_handler = default_launch_handler
alexa_blueprint.session_ended_handler = default_session_ended_handler
alexa_blueprint.force_verification = False
alexa_blueprint.app_id = None


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


@alexa_blueprint.errorhandler(InvalidRequest)
def handle_invalid_request(error):
    response = jsonify({'error': error.message})
    response.status_code = 400
    return response


@alexa_blueprint.before_request
def validate_request():
    if not current_app.debug or alexa_blueprint.force_verification:
        verify_request()

    app_id = alexa_blueprint.app_id
    incoming_app_id = flask_request.json.get(
        'session', {}).get('application', {}).get('applicationId')

    if app_id and incoming_app_id != app_id:
        raise InvalidRequest('Request contains incorrect applicationId')


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
