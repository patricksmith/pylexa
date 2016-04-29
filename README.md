# `pylexa`

*NOTE: This library is NOT ready for production use yet!*

`pylexa` is a library that aims to ease development of an [Alexa Skills Kits](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit).

`pylexa` allows one to define a simple Flask application that will be able to accept requests and return appropriate responses to the Alexa service.


## Example

Let's say you want to define an Alexa Skill that echoes whatever the user says. So far, you've:

* created a skill in the [Amazon Developer Console](https://developer.amazon.com/edw/home.html#/skills/list)
* Added a `Echo` intent with a single slot, `message`:

  ```javascript
  {
      "intent": "Echo",
      "slots": [
          {
            "name": "message",
            "type": "AMAZON.LITERAL"
          }
      ]
   }
   ```

* Added an utterance to allow users to interact with the skill:

  `Echo echo { something | message }`

Now, you're ready to create a server that will accept the request and return a response echoing the input. Using `pylexa`, we'd need only the following code to accomplish this:

```python
from flask import Flask

from pylexa.app import alexa_blueprint
from pylexa.intent import handle_intent
from pylexa.response import AlexaResponseWrapper, PlainTextSpeech


app = Flask(__name__)
app.register_blueprint(alexa_blueprint)
app.response_class = AlexaResponseWrapper


@handle_intent('Echo')
def handle_echo_intent(request):
    return PlainTextSpeech(request.slots.get('message', 'Nothing to echo'))
```

And that's it! You can push the above code, configure the skill to point to the server running the `flask` app and use the service simulator to test your skill.


## Testing

After installing requirements with `pip install -r requirements.pip`, tests can be run with `nosetests`.
