intents = {}

def handle_intent(intentName):
    def inner(func):
        intents[intentName] = func
        return func
    return inner
