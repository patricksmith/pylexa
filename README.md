# `pylexa`

`pylexa` is a library that aims to ease development of an [Alexa Skills Kits](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit).

`pylexa` allows one to define a simple Flask application that will be able to accept requests and return appropriate responses to the Alexa service.


## Example

Let's say you want to define an Alexa Skill that echoes whatever the user says. So far, you've:

  * created a skill in the [Amazon Developer Console](https://developer.amazon.com/edw/home.html#/skills/list)
  * Added an `Echo` intent with a single slot, `message`:

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
alexa_blueprint.app_id = 'my_app_id'
app.register_blueprint(alexa_blueprint)
app.response_class = AlexaResponseWrapper


@handle_intent('Echo')
def handle_echo_intent(request):
    return PlainTextSpeech(request.slots.get('message', 'Nothing to echo'))
```

And that's it! You can push the above code, configure the skill to point to the server running the `flask` app and use the service simulator to test your skill.


## Testing

After installing requirements with `pip install -r requirements.pip`, tests can be run with `nosetests`.


## Alexa Configuration

Configuration of an Alexa Skill is done in three parts in the developer console:

* the intent schema
* list of utterances
* custom slot definitions

`pylexa` comes with a command line tool that aims to simplify this configuration by allowing one to define a YAML file with the necessary information and generate the intent schema, utterances, and custom slots from that.

For example, let's say you had the following YAML schema defined:

```yaml
intents:
    - TestIntent:
        foo: AMAZON.NUMBER
        bar: CUSTOM_SLOT
    - OtherIntent
    - AMAZON.YesIntent

utterances:
    TestIntent:
        - 'do something with {foo} and {bar}'
        - '{foo} {bar}'
    OtherIntent:
        - 'do something else'

slots:
    CUSTOM_SLOT:
        - value 1
        - value 2
```

This defines a skill that handles three intents (`TestIntent`, `OtherIntent`, and `AMAZON.YesIntent`), specifies utterances for `TestIntent` and `OtherIntent`, and contains a custom slot definition.

If we have that YAML definition in `conf/schema.yml`:

```bash
$ tree conf
conf
└── schema.yml

0 directories, 1 file
```

We can then run the command line tool `generate-alexa-conf` to create the requisite files:

```bash
$ generate-alexa-conf conf/schema.yml
```

We now have the intent schema, utterances, and slots defined in their own files:

```bash
$ tree conf
conf
├── intent_schema.json
├── schema.yml
├── slots
│   ├── CUSTOM_SLOT
└── utterances.txt

1 directory, 4 files
```

The contents of each file can then be copied + pasted in to the appropriate sections of the Alexa Skill configuration.
