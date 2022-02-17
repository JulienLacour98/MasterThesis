class Action:

    def __init__(self, name, description):
        self.name = name
        self.description = description
        actions.append(self)


actions = []

# Creation of Display Fitness
DisplayFitness = Action("DF", "Display graph of a fitness function")

# Creation of Run Once
RunOnce = Action("R1", "Run an evolutionary algorithm on a fitness function ")

# Creation Run n Times
RunNTimes = Action("RN", "Run an evolutionary algorithm n times on a fitness function")




