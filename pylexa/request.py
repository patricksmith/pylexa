class Request(object):
    request = {}
    _session = {}
    is_intent = False
    is_launch = False
    is_session_ended = False

    def __init__(self, request):
        self.request = request.json.get('request', {})
        self._session = request.json.get('session', {})

    @property
    def type(self):
        return self.request.get('type')

    @property
    def timestamp(self):
        return self.request.get('timestamp')

    @property
    def request_id(self):
        return self.request.get('requestId')

    @property
    def access_token(self):
        return self._session.get('user', {}).get('accessToken')

    @property
    def session(self):
        return self._session.get('attributes', {}) or {}


class LaunchRequest(Request):

    is_launch = True


class IntentRequest(Request):

    is_intent = True
    slots = {}

    def __init__(self, request):
        super(IntentRequest, self).__init__(request)

        request_slots = self.request.get('intent', {}).get('slots', {})
        self.slots = {
            slot['name']: slot['value']
            for slot in request_slots.values() if 'value' in slot
        }

    @property
    def intent(self):
        return self.request.get('intent', {}).get('name')


class SessionEndedRequest(Request):

    is_session_ended = True

    @property
    def reason(self):
        return self.request.get('reason')
