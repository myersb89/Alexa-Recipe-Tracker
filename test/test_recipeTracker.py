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
    testinput = requestHelper.createLaunchRequest()
    testcontext = requestHelper.createLaunchContext()
    response = my_skill.invoke(testinput, testcontext)
    assert "Welcome to the Recipe Tracker" in response.to_str()

def test_newRecipe():
    testinput = requestHelper.createNewRecipeRequest()
    testcontext = requestHelper.createNewRecipeContext()
    response = my_skill.invoke(testinput,testcontext)
    assert "Ok, what should this recipe be called" in response.to_str()

def test_newRecipeProvided():
    testinput = requestHelper.createNewRecipeProvidedRequest()
    testcontext = requestHelper.createNewRecipeProvidedContext()
    response = my_skill.invoke(testinput,testcontext)
    assert "has been created" in response.to_str()
