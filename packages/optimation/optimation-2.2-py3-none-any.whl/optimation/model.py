class Variable:
    def __init__(self, name, value=0.0):
        self.name = name
        self.value = value

class Objective:
    def __init__(self, func, sense="minimize"):
        self.func = func
        self.sense = sense

    def evaluate(self, variables):
        return self.func(variables)

class Model:
    def __init__(self):
        self.variables = []
        self.objectives = []

    def add_variable(self, var):
        self.variables.append(var)

    def add_objective(self, obj):
        self.objectives.append(obj)

    def solve(self):
        results = {}
        for obj in self.objectives:
            results[obj.sense] = obj.evaluate(self.variables)
        return results
