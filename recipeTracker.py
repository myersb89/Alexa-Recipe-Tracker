import os
from ask_sdk.standard import StandardSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model.ui import SimpleCard
from recipe import recipe, ingredient
import ask_sdk_dynamodb
import boto3
import jsonpickle

#point at local dynamodb
#skill_persistence_table = os.environ["skill_persistence_table"]
skill_persistence_table = 'recipedb'
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')#, endpoint_url="http://localhost:8000")

RECIPE_SLOT = 'recipe'
SESSION_KEY = 'current_recipe'
PERSISTENCE_KEY = 'recipe_list'

sb = StandardSkillBuilder(
    table_name=skill_persistence_table, auto_create_table=False,
    partition_keygen=ask_sdk_dynamodb.partition_keygen.user_id_partition_keygen,
    dynamodb_client=dynamodb
)

def hello():
    test = "this is a test6"
    return "hello world"

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speech_text = "Welcome to the Recipe Tracker Skill. Say 'start a recipe' or 'create a recipe' to start tracking!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Launch Recipe Tracker", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response

class NewRecipeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("NewRecipeIntent")(handler_input)

    def handle(self, handler_input):

        speech_text = "Ok, what should this recipe be called?"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Recipe Tracker", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response

class NewRecipeProvidedIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("NewRecipeProvidedIntent")(handler_input)

    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes

        # check if we already have a recipe in the session. If yes, store to database before creating new.
        if SESSION_KEY in session_attr:
            persistence_attr = handler_input.attributes_manager.persistent_attributes
            persistence_attr[PERSISTENCE_KEY] = session_attr[SESSION_KEY]
            handler_input.attributes_manager.save_persistent_attributes()

        # Get the recipe name provided from the slot. Create a recipe object and save to session.
        slots = handler_input.request_envelope.request.intent.slots
        recipe_name = slots[RECIPE_SLOT].value
        session_attr[SESSION_KEY] = jsonpickle.encode(recipe(recipe_name))

        speech_text = "Recipe has been created. Say 'add ingredient' to add an ingredient to the recipe."

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Recipe Tracker", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "Recipe Tracker lets you record ingredients as you cook so you can easily track the calories and macros. Say 'start a recipe' or 'create a recipe' to get started."

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Recipe Tracker", speech_text))
        return handler_input.response_builder.response

class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Recipe Tracker", speech_text))
        return handler_input.response_builder.response

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        #any cleanup logic goes here.
        return handler_input.response_builder.response

class AllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        #log exception in CloudWatch logs
        print(exception)

        speech_text = "Sorry, I didn't get it. Can you please say it again?"
        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_request_handler(NewRecipeIntentHandler())
sb.add_request_handler(NewRecipeProvidedIntentHandler())

sb.add_exception_handler(AllExceptionHandler())

handler = sb.lambda_handler()