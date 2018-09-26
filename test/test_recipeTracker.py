#Append to sys.path so Python can find my file in the parent directory
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import recipeTracker
from ask_sdk_core.handler_input import HandlerInput
import requestHelper

def test_hello():
    assert recipeTracker.hello() == 'hello world'

def test_launchCanHandle():
    testLaunchHandler = recipeTracker.LaunchRequestHandler()
    testinput = requestHelper.createLaunchRequest()
    assert testLaunchHandler.can_handle(HandlerInput(testinput)) == True

def test_newRecipeCanHandle():
    testNewRecipeHandler = recipeTracker.NewRecipeIntentHandler()
    testinput = requestHelper.createNewRecipeRequest()
    assert testNewRecipeHandler.can_handle(HandlerInput(testinput)) == True

def test_newRecipeHandle():
    testNewRecipeHandler = recipeTracker.NewRecipeIntentHandler()
    testinput = requestHelper.createNewRecipeRequest()

    response = testNewRecipeHandler.handle(HandlerInput(testinput))

    assert testNewRecipeHandler.can_handle(HandlerInput(testinput)) == True

