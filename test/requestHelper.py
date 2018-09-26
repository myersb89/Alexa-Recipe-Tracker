from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_model import request_envelope
import json

sb = SkillBuilder()
skill_obj = sb.create()

def createLaunchRequest():
    with open("samples\\launchrequest.json") as json_file:
        data = json.load(json_file)
        return skill_obj.serializer.deserialize(payload=json.dumps(data), obj_type=request_envelope.RequestEnvelope)

def createNewRecipeRequest():
    with open("samples\\newreciperequest.json") as json_file:
        data = json.load(json_file)
        return skill_obj.serializer.deserialize(payload=json.dumps(data), obj_type=request_envelope.RequestEnvelope)