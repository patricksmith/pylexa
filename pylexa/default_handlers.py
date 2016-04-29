from pylexa.response import PlainTextSpeech, Response


def default_launch_handler(request):
    return PlainTextSpeech('Launching...')


def default_session_ended_handler(request):
    return Response()


def default_unrecognized_intent_handler(request):
    return PlainTextSpeech("I'm sorry, I didn't understand that")
