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

def test_sessionEnded():
    testinput, testcontext = requestHelper.requestBuilder(request_type="SessionEndedRequest")
    response = my_skill.invoke(testinput, testcontext)
    response_dict = response.to_dict()
    assert response_dict["response"]["output_speech"] is None

def test_sessionEndedWithSessionAttr():
    testinput, testcontext = requestHelper.requestBuilder(request_type="SessionEndedRequest",attributes="Scrambled Eggs")
    response = my_skill.invoke(testinput, testcontext)
    response_dict = response.to_dict()
    assert response_dict["response"]["output_speech"] is None

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
    testinput, testcontext = requestHelper.requestBuilder(request_type="SessionEndedRequest", attributes="Pizza")
    response = my_skill.invoke(testinput, testcontext)
    slots = requestHelper.slotBuilder({"recipe": "Pizza"})
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="NewRecipeProvidedIntent", slots=slots)
    response = my_skill.invoke(testinput, testcontext)
    assert "That recipe already exists" in response.to_str()

def test_deleteRecipeExistsInDb():
    testinput, testcontext = requestHelper.requestBuilder(request_type="SessionEndedRequest", attributes="Sphagetti")
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
    testinput, testcontext = requestHelper.requestBuilder(request_type="SessionEndedRequest", attributes="Fish Sticks")
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
    slots = requestHelper.slotBuilder({"ingredient": "sugar", "amount": None, "measurement": None})
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="AddIngredientIntent", slots=slots, dialog_state="COMPLETED")
    response = my_skill.invoke(testinput, testcontext)
    assert "not currently tracking" in response.to_str()

def test_addIngredientMissingIngredient():
    slots = requestHelper.slotBuilder({"ingredient": None,"amount": None, "measurement": None})
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="AddIngredientIntent", slots=slots, dialog_state="STARTED")
    response = my_skill.invoke(testinput, testcontext)
    assert "what ingredient would" in response.to_str()

def test_addIngredientMissingAmount():
    slots = requestHelper.slotBuilder({"ingredient": "carrots", "amount": None, "measurement": None})
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="AddIngredientIntent", slots=slots, dialog_state="STARTED")
    response = my_skill.invoke(testinput, testcontext)
    assert "what amount " in response.to_str()

def test_addIngredientMissingMeasurement():
    slots = requestHelper.slotBuilder({"ingredient": "beans", "amount": "one", "measurement": None})
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="AddIngredientIntent", slots=slots, dialog_state="STARTED")
    response1 = my_skill.invoke(testinput, testcontext)
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="AddIngredientIntent", attributes="Jello", slots=slots,
                                                          dialog_state="COMPLETED")
    response2 = my_skill.invoke(testinput, testcontext)
    assert "Dialog.Delegate" in response1.to_str() and "has been added" in response2.to_str()

def test_addIngredientAllSlots():
    slots = requestHelper.slotBuilder({"ingredient": "potato", "amount": "2", "measurement": "pounds"})
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="AddIngredientIntent", attributes="Pot Roast", slots=slots, dialog_state="COMPLETED")
    response = my_skill.invoke(testinput, testcontext)
    assert "has been added" in response.to_str()

def test_addTwoIngredients():
    slots = requestHelper.slotBuilder({"ingredient": "cheese", "amount": "2", "measurement": "ounces"})
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="AddIngredientIntent", attributes="Fritata", slots=slots, dialog_state="COMPLETED")
    response1 = my_skill.invoke(testinput, testcontext)
    slots = requestHelper.slotBuilder({"ingredient": "eggs", "amount": "6", "measurement": None})
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="AddIngredientIntent", attributes="Fritata",
                                                          slots=slots, dialog_state="COMPLETED")
    response2 = my_skill.invoke(testinput, testcontext)
    assert "has been added" in response1.to_str() and "has been added" in response2.to_str()

def test_readRecipeProvidedNoIngredients():
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="ReadRecipeIntent", attributes="Pot Roast")
    response = my_skill.invoke(testinput, testcontext)
    assert "This recipe has no ingredients" in response.to_str()

def test_readRecipeProvidedWithIngredients():
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="ReadRecipeIntent", ingredient="carrot", attributes="Pot Roast")
    response = my_skill.invoke(testinput, testcontext)
    assert "pounds carrot" in response.to_str()

#test_readRecipeProvidedWithIngredients()
