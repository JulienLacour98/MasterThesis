class Action:

    def __init__(self, name, description):
        self.name = name
        self.description = description
        actions.append(self)


actions = []

# Creation of Display Fitness
DisplayFitness = Action("DF", "Display the graph of a fitness function")

# Creation of Run Once
RunOnce = Action("R1", "Display a run of an evolutionary algorithm on a fitness function")

# Creation of Run n Times
RunNTimes = Action("RN",
                   "Statistical analysis of an evolutionary algorithm on a fitness function and fixed problem size")

# Creation of Run or a range of problem sizes
RunFromNtoM = Action("RNM",
                     "Statistical analysis of one evolutionary algorithm on a fitness function "
                     "for a range of problem sizes")

# Creation of Run k fitness function for a range of problem sizes
RunKFromNtoM = Action("RKNM",
                      "Comparison of several evolutionary algorithms on a fitness function "
                      "for a range of problem sizes")




