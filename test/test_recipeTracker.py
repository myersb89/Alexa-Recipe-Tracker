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

def test_deleteRecipeExistsInDb():
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                              intent_name="AMAZON.StopIntent", attributes="Sphagetti")
    response = my_skill.invoke(testinput, testcontext)
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="DeleteRecipeIntent", slot_name="recipe", slot_value="Sphagetti")
    response = my_skill.invoke(testinput, testcontext)
    assert "recipe has been deleted" in response.to_str()

def test_deleteRecipeExistsInSession():
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="DeleteRecipeIntent", attributes="Pot Roast", slot_name="recipe", slot_value="Pot Roast")
    response = my_skill.invoke(testinput, testcontext)
    assert "recipe has been deleted" in response.to_str()

def test_deleteRecipeNotExists():
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="DeleteRecipeIntent", slot_name="recipe", slot_value="Salmon")
    response = my_skill.invoke(testinput, testcontext)
    assert "could not find" in response.to_str()

def test_loadRecipeExists():
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="AMAZON.StopIntent", attributes="Fish Sticks")
    response = my_skill.invoke(testinput, testcontext)
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="LoadRecipeIntent", slot_name="recipe", slot_value="Fish Sticks")
    response = my_skill.invoke(testinput, testcontext)
    assert "recipe has been loaded" in response.to_str()

def test_loadRecipeNotExists():
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="LoadRecipeIntent", slot_name="recipe", slot_value="Peking Duck")
    response = my_skill.invoke(testinput, testcontext)
    assert "could not find" in response.to_str()

def test_addIngredientRecipeNotLoaded():
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest",
                                                          intent_name="AddIngredientIntent", slot_name="ingredient", slot_value="sugar")
    response = my_skill.invoke(testinput, testcontext)
    assert "not currently tracking" in response.to_str()

#test_newRecipeProvidedAlreadyExistsInDb()