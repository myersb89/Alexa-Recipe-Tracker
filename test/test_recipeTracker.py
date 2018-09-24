#Append to sys.path so Python can find my file in the parent directory
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import recipeTracker
import json
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import request
from ask_sdk_model import request_envelope

def test_hello():
    assert recipeTracker.hello() == 'hello world'

def test_launch():
    testLaunch = recipeTracker.LaunchRequestHandler()
    j = """{
      "session": {
        "new": true,
        "sessionId": "amzn1.echo-api.session.[unique-value-here]",
        "attributes": {},
        "user": {
          "userId": "amzn1.ask.account.[unique-value-here]"
        },
        "application": {
          "applicationId": "amzn1.ask.skill.[unique-value-here]"
        }
      },
      "version": "1.0",
      "request": {
        "locale": "en-US",
        "timestamp": "2016-10-27T18:21:44Z",
        "type": "LaunchRequest",
        "requestId": "amzn1.echo-api.request.[unique-value-here]"
      },
      "context": {
        "AudioPlayer": {
          "playerActivity": "IDLE"
        },
        "System": {
          "device": {
            "supportedInterfaces": {
              "AudioPlayer": {}
            }
          },
          "application": {
            "applicationId": "amzn1.ask.skill.[unique-value-here]"
          },
          "user": {
            "userId": "amzn1.ask.account.[unique-value-here]"
          }
        }
      }
    }"""
    dsj = json.loads(j)

    #type,request_id,timestamp,locale
    testreq = request.Request(dsj['request']['type'],dsj['request']['requestId'],dsj['request']['timestamp'],dsj['request']['locale'])

    #envelope(version, session,context,request)
    testreqenv = request_envelope.RequestEnvelope(request=testreq)

    input = HandlerInput(testreqenv)

    assert testLaunch.can_handle(input) == True