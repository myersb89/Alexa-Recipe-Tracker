from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_model import request_envelope
from ask_sdk_model import context
import json

sb = SkillBuilder()
skill_obj = sb.create()

def requestBuilder(request_type, attributes = None, intent_name = None, slots = None, ingredient = None, dialog_state = None, userid = "amzn1.ask.account.[unique-value-here]"):
    #input: userid, request type, session attributes
    session = {}
    session["new"] = True
    session["sessionId"] = "amzn1.echo-api.session.[unique-value-here]"
    if attributes == None:
        session["attributes"] = {}

    else:
        if ingredient == None:
            session["attributes"] = {"current_recipe": "{\"py/object\": \"recipe.recipe\", \"directions\": [], \"ingredients\": {\"py/set\": []}, \"title\": \"" + attributes + "\"}"}
        else:
            session["attributes"] = {
                "current_recipe": "{\"py/object\": \"recipe.recipe\", \"directions\": [], \"ingredients\": {\"py/set\": [{\"py/object\": \"recipe.ingredient\", \"amount\": \"2\", \"item\": \"" + ingredient + "\", \"measurement\": \"pounds\"}]}, \"title\": \"" + attributes + "\"}"}
            '''"current_recipe": "{\"py/object\": \"recipe.recipe\", \"directions\": [], \"ingredients\": {\"py/set\": [{\"py/object\": \"recipe.ingredient\", \"amount\": \"2\", \"item\": \"potatoes\", \"measurement\": null}, {\"py/object\": \"recipe.ingredient\", \"amount\": \"2\", \"item\": \"mustard\", \"measurement\": \"grams\"}]}, \"title\": \"potato salad\"}"'''
    session["user"] = {"userId": userid}
    request = {}
    request["locale"] = "en-US"
    request["timestamp"] = "2016-10-27T18:21:44Z"
    request["type"] = request_type
    request["requestId"] = "amzn1.echo-api.request.[unique-value-here]"
    if intent_name != None:
        request["intent"] = {"name": intent_name, "confirmationStatus": "NONE"}

        if slots != None:
            request["intent"]["slots"] = slots
            '''
            for s_name, s in slots.items():
                request["intent"]["slots"][s_name] = s
        if slot_name != None and slot_value != None:
            request["intent"]["slots"] = {slot_name: {"name": slot_name, "value": slot_value, "confirmationStatus": "NONE"}}
        elif slot_name != None and slot_value == None:
            request["intent"]["slots"] = {
                slot_name: {"name": slot_name, "confirmationStatus": "NONE"}}'''

    if dialog_state != None:
        request["dialogState"] = dialog_state
    con = {}
    con["AudioPlayer"] = {"playerActivity": "IDLE"}
    con["System"] = {"device": {"supportedInterfaces": {"AudioPlayer": {}}}, "application":{"applicationId": "amzn1.ask.skill.[unique-value-here]"}, "user":{"userId": "amzn1.ask.account.[unique-value-here]"}}
    data = {"session": session, "version": "1.0", "request": request, "context": con}

    return skill_obj.serializer.deserialize(payload=json.dumps(data), obj_type=request_envelope.RequestEnvelope), skill_obj.serializer.deserialize(payload=json.dumps(data), obj_type=context.Context)

def slotBuilder(names):
    slots = {}
    for name, value in names.items():
        if value != None:
            slots[name] = {"name": name, "value": value, "confirmationStatus": "NONE"}
        else:
            slots[name] = {"name": name, "confirmationStatus": "NONE"}
    return slots

def sessionAttrBuilder():
    return

#TO do
#getSsmlFromResponse
#getSessionAttrFromResponse
