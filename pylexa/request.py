class Request(object):
    request = {}
    is_intent = False
    is_launch = False
    is_session_ended = False

    def __init__(self, request):
        self.request = request.json.get('request', {})

    @property
    def type(self):
        return self.request.get('type')

    @property
    def timestamp(self):
        return self.request.get('timestamp')

    @property
    def requestId(self):
        return self.request.get('requestId')


class LaunchRequest(Request):

    is_launch = True


class IntentRequest(Request):

    is_intent = True

    @property
    def intent(self):
        return self.request.get('intent', {}).get('name')

    @property
    def slots(self):
        slots = self.request.get('intent', {}).get('slots', {})
        return {
            slot['name']: slot['value']
            for slot in slots.values()
        }


class SessionEndedRequest(Request):

    is_session_ended = True

    @property
    def reason(self):
        return self.request.get('reason')
