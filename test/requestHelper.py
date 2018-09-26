from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_model import request_envelope
from ask_sdk_model import context
import json

sb = SkillBuilder()
skill_obj = sb.create()

def requestBuilder(request_type, attributes = None, intent_name = None, slot_name = None, slot_value = None, userid = "amzn1.ask.account.[unique-value-here]"):
    #input: userid, request type, session attributes
    session = {}
    session["new"] = True
    session["sessionId"] = "amzn1.echo-api.session.[unique-value-here]"
    if attributes == None:
        session["attributes"] = {}

    else:
        session["attributes"] = {"current_recipe": "{\"py/object\": \"recipe.recipe\", \"directions\": [], \"ingredients\": {\"py/set\": []}, \"title\": \"" + attributes + "\"}"}
    session["user"] = {"userId": userid}
    request = {}
    request["locale"] = "en-US"
    request["timestamp"] = "2016-10-27T18:21:44Z"
    request["type"] = request_type
    request["requestId"] = "amzn1.echo-api.request.[unique-value-here]"
    if intent_name != None:
        request["intent"] = {"name": intent_name, "confirmationStatus": "NONE"}
        if slot_name != None:
            request["intent"]["slots"] = {slot_name: {"name": slot_name, "value": slot_value, "confirmationStatus": "NONE"}}
    con = {}
    con["AudioPlayer"] = {"playerActivity": "IDLE"}
    con["System"] = {"device": {"supportedInterfaces": {"AudioPlayer": {}}}, "application":{"applicationId": "amzn1.ask.skill.[unique-value-here]"}, "user":{"userId": "amzn1.ask.account.[unique-value-here]"}}
    data = {"session": session, "version": "1.0", "request": request, "context": con}

    return skill_obj.serializer.deserialize(payload=json.dumps(data), obj_type=request_envelope.RequestEnvelope), skill_obj.serializer.deserialize(payload=json.dumps(data), obj_type=context.Context)


#TO do
#getSsmlFromResponse
#getSessionAttrFromResponse