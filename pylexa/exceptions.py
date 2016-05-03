class InvalidRequest(Exception):
    """The request was deemed invalid according to Amazon's guidelines:
    https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/developing-an-alexa-skill-as-a-web-service#Verifying that the Request was Sent by Alexa
    """

    pass
