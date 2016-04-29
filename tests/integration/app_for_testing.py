from flask import Flask

from pylexa.app import alexa_blueprint, handle_launch_request, handle_session_ended_request
from pylexa.intent import handle_intent
from pylexa.response import AlexaResponseWrapper, LinkAccountCard, PlainTextSpeech, Response


@handle_launch_request
def handle_launch(request):
    return PlainTextSpeech('This is my launch handler')


@handle_session_ended_request
def handle_session_ended(request):
    return PlainTextSpeech('Later, alligator')


@handle_intent('Echo')
def handle_echo_intent(request):
    return PlainTextSpeech(request.slots.get('message', 'Nothing to echo'))


@handle_intent('RequiresAuth')
def handle_auth_intent(request):
    return Response(
        speech=PlainTextSpeech('You need to link your account first'),
        card=LinkAccountCard()
    )


app = Flask(__name__)
app.register_blueprint(alexa_blueprint)
app.response_class = AlexaResponseWrapper
