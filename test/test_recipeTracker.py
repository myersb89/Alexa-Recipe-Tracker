#Append to sys.path so Python can find my file in the parent directory
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import recipeTracker
from ask_sdk_core.handler_input import HandlerInput
import requestHelper

my_skill = recipeTracker.sb.create()

def test_hello():
    assert recipeTracker.hello() == 'hello world'

def test_launch():
    testinput, testcontext = requestHelper.requestBuilder("LaunchRequest")
    response = my_skill.invoke(testinput, testcontext)
    assert "Welcome to the Recipe Tracker" in response.to_str()

def test_newRecipe():
    testinput, testcontext = requestHelper.requestBuilder("IntentRequest", "NewRecipeIntent")
    response = my_skill.invoke(testinput,testcontext)
    assert "Ok, what should this recipe be called" in response.to_str()

def test_newRecipeProvided():
    testinput, testcontext = requestHelper.requestBuilder(request_type="IntentRequest", intent_name="NewRecipeProvidedIntent", slot_name="recipe", slot_value="Mac and cheese")
    response = my_skill.invoke(testinput,testcontext)
    assert "has been created" in response.to_str()
