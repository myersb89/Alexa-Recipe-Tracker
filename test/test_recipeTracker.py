#Append to sys.path so Python can find my file in the parent directory
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import recipeTracker
from ask_sdk_core.handler_input import HandlerInput
import requestHelper

my_skill = recipeTracker.sb.create()

def test_launch():
    testinput, testcontext = requestHelper.requestBuilder(request_type="LaunchRequest")
    response = my_skill.invoke(testinput, testcontext)
    assert "Welcome to the Recipe Tracker" in response.to_str()

def test_newRecipe():
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest", intent_name="NewRecipeIntent")
    response = my_skill.invoke(testinput,testcontext)
    assert "Ok, what should this recipe be called" in response.to_str()

def test_newRecipeProvided():
    slots = requestHelper.slotBuilder({"recipe": "Mac and cheese"})
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest", intent_name="NewRecipeProvidedIntent", slots=slots)
    response = my_skill.invoke(testinput,testcontext)
    assert "has been created" in response.to_str()

def test_stopNoSession():
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="AMAZON.StopIntent")
    response = my_skill.invoke(testinput, testcontext)
    assert "Goodbye" in response.to_str()

def test_stopWithSession():
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="AMAZON.StopIntent", attributes="Beef Stew")
    response = my_skill.invoke(testinput, testcontext)
    assert "Goodbye" in response.to_str()

def test_newRecipeProvidedAlreadyExistsInSession():
    slots = requestHelper.slotBuilder({"recipe": "Mac and cheese"})
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest", attributes="Mac and cheese",
                                                          intent_name="NewRecipeProvidedIntent", slots=slots)
    response = my_skill.invoke(testinput, testcontext)
    assert "That recipe already exists" in response.to_str()

def test_newRecipeProvidedAlreadyExistsInDb():
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="AMAZON.StopIntent", attributes="Pizza")
    response = my_skill.invoke(testinput, testcontext)
    slots = requestHelper.slotBuilder({"recipe": "Pizza"})
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="NewRecipeProvidedIntent", slots=slots)
    response = my_skill.invoke(testinput, testcontext)
    assert "That recipe already exists" in response.to_str()

def test_deleteRecipeExistsInDb():
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                              intent_name="AMAZON.StopIntent", attributes="Sphagetti")
    response = my_skill.invoke(testinput, testcontext)
    slots = requestHelper.slotBuilder({"recipe": "Sphagetti"})
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="DeleteRecipeIntent", slots=slots)
    response = my_skill.invoke(testinput, testcontext)
    assert "recipe has been deleted" in response.to_str()

def test_deleteRecipeExistsInSession():
    slots = requestHelper.slotBuilder({"recipe": "Pot Roast"})
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="DeleteRecipeIntent", attributes="Pot Roast", slots=slots)
    response = my_skill.invoke(testinput, testcontext)
    assert "recipe has been deleted" in response.to_str()

def test_deleteRecipeNotExists():
    slots = requestHelper.slotBuilder({"recipe": "Salmon"})
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="DeleteRecipeIntent", slots=slots)
    response = my_skill.invoke(testinput, testcontext)
    assert "could not find" in response.to_str()

def test_loadRecipeExists():
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="AMAZON.StopIntent", attributes="Fish Sticks")
    response = my_skill.invoke(testinput, testcontext)
    slots = requestHelper.slotBuilder({"recipe": "Fish Sticks"})
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="LoadRecipeIntent", slots=slots)
    response = my_skill.invoke(testinput, testcontext)
    assert "recipe has been loaded" in response.to_str()

def test_loadRecipeNotExists():
    slots = requestHelper.slotBuilder({"recipe": "Peking Duck"})
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="LoadRecipeIntent", slots=slots)
    response = my_skill.invoke(testinput, testcontext)
    assert "could not find" in response.to_str()

def test_addIngredientRecipeNotLoaded():
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="AddIngredientIntent", slot_name="ingredient", slot_value="sugar", dialog_state="COMPLETED")
    response = my_skill.invoke(testinput, testcontext)
    assert "not currently tracking" in response.to_str()

def test_addIngredientMissingIngredient():
    slots = requestHelper.slotBuilder({"ingredient": None})
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="AddIngredientIntent", slots=slots, dialog_state="STARTED")
    response = my_skill.invoke(testinput, testcontext)
    assert "would you like to add" in response.to_str()

def test_addIngredientMissingAmount():
    slots = requestHelper.slotBuilder({"ingredient": "carrots", "amount": None})
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="AddIngredientIntent", slots=slots, dialog_state="STARTED")
    response = my_skill.invoke(testinput, testcontext)
    assert "what amount " in response.to_str()

def test_addIngredientMissingMeasurement():
    slots = requestHelper.slotBuilder({"ingredient": "beans", "amount": "one", "measurement": None})
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="AddIngredientIntent", slots=slots, dialog_state="STARTED")
    response = my_skill.invoke(testinput, testcontext)
    assert "Not implemented " in response.to_str()

def test_addIngredientAllSlots():
    slots = requestHelper.slotBuilder({"ingredient": "potato", "amount": "2", "measurement": "pounds"})
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="AddIngredientIntent", attributes="Pot Roast", slots=slots, dialog_state="COMPLETED")
    response = my_skill.invoke(testinput, testcontext)
    assert "Not implemented" in response.to_str()

test_addIngredientMissingMeasurement()