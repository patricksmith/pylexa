from flask import Blueprint

from pylexa.default_handlers import (
    default_launch_handler,
    default_session_ended_handler,
)
from pylexa.response import AlexaResponseWrapper


class BlueprintWithAlexaResponseClass(Blueprint):
    def register(self, app, options, first_registration=False):
        app.response_class = AlexaResponseWrapper

        super(BlueprintWithAlexaResponseClass,
              self).register(app, options, first_registration)


alexa_blueprint = BlueprintWithAlexaResponseClass('alexa', __name__)
alexa_blueprint.launch_handler = default_launch_handler
alexa_blueprint.session_ended_handler = default_session_ended_handler

