import os
from ask_sdk.standard import StandardSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import DialogState
from ask_sdk_model.dialog import (ElicitSlotDirective, DelegateDirective)
from recipe import recipe, ingredient
import ask_sdk_dynamodb
import boto3
import jsonpickle

#point at local dynamodb
#skill_persistence_table = os.environ["skill_persistence_table"]
skill_persistence_table = 'recipedb'
dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")

RECIPE_SLOT = 'recipe'
INGREDIENT_SLOT = 'ingredient'
SESSION_KEY = 'current_recipe'
PERSISTENCE_KEY = 'recipe_list'

sb = StandardSkillBuilder(
    table_name=skill_persistence_table, auto_create_table=False,
    partition_keygen=ask_sdk_dynamodb.partition_keygen.user_id_partition_keygen,
    dynamodb_client=dynamodb
)

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
        # Get the recipe name provided from the slot.
        slots = handler_input.request_envelope.request.intent.slots
        recipe_name = slots[RECIPE_SLOT].value

        session_attr = handler_input.attributes_manager.session_attributes
        persistence_attr = handler_input.attributes_manager.persistent_attributes
        existing_recipe_list = None

        #check if recipe already exists in db
        if PERSISTENCE_KEY in persistence_attr:
            existing_recipe_list = persistence_attr[PERSISTENCE_KEY]
            for i in existing_recipe_list:
                item = jsonpickle.decode(i)
                if item.title == recipe_name:
                    speech_text = "That recipe already exists."
                    handler_input.response_builder.speak(speech_text).set_card(
                        SimpleCard("Recipe Tracker", speech_text)).set_should_end_session(
                        False)
                    return handler_input.response_builder.response

        #if we have a recipe in session
        if SESSION_KEY in session_attr:
            cur_recipe = jsonpickle.decode(session_attr[SESSION_KEY])

            #check if it's the same as we are trying to add
            if cur_recipe.title == recipe_name:
                speech_text = "That recipe already exists."
                handler_input.response_builder.speak(speech_text).set_card(
                    SimpleCard("Recipe Tracker", speech_text)).set_should_end_session(
                    False)
                return handler_input.response_builder.response
            #if it's not, save current recipe to database
            else:
                saveSessionToDb(session_attr, persistence_attr, handler_input)

        #save recipe to session as the current recipe
        session_attr[SESSION_KEY] = jsonpickle.encode(recipe(recipe_name))

        speech_text = "Recipe has been created. Say 'add ingredient' to add an ingredient to the recipe."

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Recipe Tracker", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response

class DeleteRecipeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("DeleteRecipeIntent")(handler_input)

    def handle(self, handler_input):
        # Get the recipe name provided from the slot.
        slots = handler_input.request_envelope.request.intent.slots
        recipe_name = slots[RECIPE_SLOT].value
        speech_text = "Sorry, I could not find a recipe called " + recipe_name

        session_attr = handler_input.attributes_manager.session_attributes
        persistence_attr = handler_input.attributes_manager.persistent_attributes

        # delete from database
        if PERSISTENCE_KEY in persistence_attr:
            existing_recipe_list = persistence_attr[PERSISTENCE_KEY]
            for i in existing_recipe_list:
                item = jsonpickle.decode(i)
                if item.title == recipe_name:
                    existing_recipe_list.remove(i)
                    speech_text = recipe_name + " recipe has been deleted."
                    handler_input.attributes_manager.save_persistent_attributes()
                    break

        #delete from session
        if SESSION_KEY in session_attr:
            cur_recipe = jsonpickle.decode(session_attr[SESSION_KEY])
            if cur_recipe.title == recipe_name:
                handler_input.attributes_manager.session_attributes = {}
                speech_text = recipe_name + " recipe has been deleted."

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Recipe Tracker", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response

class LoadRecipeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("LoadRecipeIntent")(handler_input)

    def handle(self, handler_input):
        # Get the recipe name provided from the slot.
        slots = handler_input.request_envelope.request.intent.slots
        recipe_name = slots[RECIPE_SLOT].value
        speech_text = "Sorry, I could not find a recipe called " + recipe_name

        session_attr = handler_input.attributes_manager.session_attributes
        persistence_attr = handler_input.attributes_manager.persistent_attributes

        # load from database
        if PERSISTENCE_KEY in persistence_attr:
            existing_recipe_list = persistence_attr[PERSISTENCE_KEY]
            for i in existing_recipe_list:
                item = jsonpickle.decode(i)
                if item.title == recipe_name:
                    ##If we find the recipe to load in the db, Save current session to db
                    saveSessionToDb(session_attr, persistence_attr, handler_input)

                    #load recipe it into the session
                    session_attr[SESSION_KEY] = jsonpickle.encode(item)
                    speech_text = recipe_name + " recipe has been loaded."
                    break

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Recipe Tracker", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response

class AddIngredientCompletedIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (is_intent_name("AddIngredientIntent")(handler_input) and handler_input.request_envelope.request.dialog_state == DialogState.COMPLETED)

    def handle(self, handler_input):
        # Get the recipe name provided from the slot.
        #slots = handler_input.request_envelope.request.intent.slots
        #recipe_name = slots[RECIPE_SLOT].value

        session_attr = handler_input.attributes_manager.session_attributes
        if SESSION_KEY not in session_attr:
            speech_text = "You are not currently tracking a recipe. Say 'create recipe' to start tracking a new recipe or 'load recipe' to work on an existing recipe"
            handler_input.response_builder.speak(speech_text).set_card(
                SimpleCard("Recipe Tracker", speech_text)).set_should_end_session(
                False)
            return handler_input.response_builder.response

        #at this point I should have values for all my slots
        slots = handler_input.request_envelope.request.intent.slots
        new_ingredient = ingredient(item=slots['ingredient'].value, amount=slots['amount'].value, measurement=slots['measurement'].value)
        cur_recipe = jsonpickle.decode(session_attr[SESSION_KEY])
        cur_recipe.addIngredient(new_ingredient)
        session_attr[SESSION_KEY] = jsonpickle.encode(cur_recipe)
        handler_input.attributes_manager.session_attributes = session_attr

        speech_text = str(new_ingredient) + " has been added to " + cur_recipe.title
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Recipe Tracker", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response

class AddIngredientInProgressIntentHandler(AbstractRequestHandler):
        def can_handle(self, handler_input):
            return (is_intent_name("AddIngredientIntent")(handler_input) and handler_input.request_envelope.request.dialog_state != DialogState.COMPLETED)

        def handle(self, handler_input):
            slots = handler_input.request_envelope.request.intent.slots
            if 'ingredient' in slots.keys() and slots['ingredient'].value == None:
                prompt = "Ok, what ingredient would you like to add?"
                return handler_input.response_builder.speak(
                    prompt).ask(prompt).add_directive(
                    ElicitSlotDirective(slot_to_elicit='ingredient')
                ).response
            elif 'amount' in slots.keys() and slots['amount'].value == None:
                prompt = "Ok, what amount should I add?"
                return handler_input.response_builder.speak(
                    prompt).ask(prompt).add_directive(
                    ElicitSlotDirective(slot_to_elicit='amount')
                ).response

            return handler_input.response_builder.add_directive(
                DelegateDirective(
                    updated_intent=handler_input.request_envelope.request.intent
                )).response


class ReadRecipeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("ReadRecipeIntent")(handler_input)

    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        if SESSION_KEY not in session_attr:
            speech_text = "You are not currently tracking a recipe. Say 'create recipe' to start tracking a new recipe or 'load recipe' to work on an existing recipe"
            handler_input.response_builder.speak(speech_text).set_card(
                SimpleCard("Recipe Tracker", speech_text)).set_should_end_session(
                False)
            return handler_input.response_builder.response
        else:
            cur_recipe = jsonpickle.decode(session_attr[SESSION_KEY])
            speech_text = str(cur_recipe)
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
        session_attr = handler_input.attributes_manager.session_attributes
        persistence_attr = handler_input.attributes_manager.persistent_attributes
        saveSessionToDb(session_attr, persistence_attr, handler_input)
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Recipe Tracker", speech_text)).set_should_end_session(True)
        return handler_input.response_builder.response

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        persistence_attr = handler_input.attributes_manager.persistent_attributes
        saveSessionToDb(session_attr, persistence_attr, handler_input)

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

def saveSessionToDb(session_attr, persistence_attr, handler_input):
    if SESSION_KEY in session_attr:
        if PERSISTENCE_KEY in persistence_attr:
            cur_recipe = jsonpickle.decode(session_attr[SESSION_KEY])
            existing_recipe_list = persistence_attr[PERSISTENCE_KEY]
            found = False
            for inx, i in enumerate(existing_recipe_list):
                item = jsonpickle.decode(i)
                if item.title == cur_recipe.title:
                    existing_recipe_list[inx] = jsonpickle.encode(cur_recipe)
                    found = True
            if found == False:
                existing_recipe_list.append(session_attr[SESSION_KEY])
                persistence_attr[PERSISTENCE_KEY] = existing_recipe_list
        else:
            new_recipe_list = [session_attr[SESSION_KEY]]
            persistence_attr[PERSISTENCE_KEY] = new_recipe_list
        handler_input.attributes_manager.save_persistent_attributes()


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_request_handler(NewRecipeIntentHandler())
sb.add_request_handler(NewRecipeProvidedIntentHandler())
sb.add_request_handler(DeleteRecipeIntentHandler())
sb.add_request_handler(LoadRecipeIntentHandler())
sb.add_request_handler(AddIngredientCompletedIntentHandler())
sb.add_request_handler(AddIngredientInProgressIntentHandler())
sb.add_request_handler(ReadRecipeIntentHandler())

sb.add_exception_handler(AllExceptionHandler())

handler = sb.lambda_handler()