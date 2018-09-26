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
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest", intent_name="NewRecipeProvidedIntent", slot_name="recipe", slot_value="Mac and cheese")
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
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest", intent_name="NewRecipeProvidedIntent", slot_name="recipe", slot_value="Mac and cheese")
    response = my_skill.invoke(testinput,testcontext)
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest", attributes="Mac and cheese",
                                                          intent_name="NewRecipeProvidedIntent", slot_name="recipe",
                                                          slot_value="Mac and cheese")
    response = my_skill.invoke(testinput, testcontext)
    assert "That recipe already exists" in response.to_str()

def test_newRecipeProvidedAlreadyExistsInDb():
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="AMAZON.StopIntent", attributes="Pizza")
    response = my_skill.invoke(testinput, testcontext)
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="NewRecipeProvidedIntent", slot_name="recipe",
                                                          slot_value="Pizza")
    response = my_skill.invoke(testinput, testcontext)
    assert "That recipe already exists" in response.to_str()

#test_newRecipeProvidedAlreadyExistsInDb()