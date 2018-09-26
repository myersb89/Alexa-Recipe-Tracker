#Class definitions for my recipe and ingredient class.
#Recipe consists of a string title, set of ingredients, and a list of directions.
#Ingredients consist of an item, amount and an optional measurement.

class recipe:
    def __init__(self,title):
        self.title = title
        #ingredients {'item':'amount'
        self.ingredients = set()
        self.directions = []

    def __repr__(self):
        return self.title

    def addIngredient(self, ingredient):
        self.ingredients.add(ingredient)

class ingredient:
    def __init__(self, item, amount, measurement=None):
        self.item = item
        self.amount = amount
        self.measurement = measurement

    def __repr__(self):
        output = []
        output.append(str(self.amount) + " ")
        if self.measurement != None:
            output.append(self.measurement + " ")
        output.append(self.item)
        return "".join(output)

