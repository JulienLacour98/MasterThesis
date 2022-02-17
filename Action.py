from matplotlib import pyplot as plt

from EvolutionaryAlgorithm import *
from FitnessFunction import *
from Utilities import *


class Action:

    def __init__(self, name, description,  parameters):
        self.name = name
        self.description = description
        self.parameters = parameters
        actions.append(self)


actions = []

# Creation of Display Fitness
DisplayFitness = Action("DF", "Display graph of a fitness function", [])

# Creation of Run Once
RunOnce = Action("R1", "Run an evolutionary algorithm on a fitness function ", [])

# Creation Run n Times
RunNTimes = Action("RN", "Run an evolutionary algorithm n times on a fitness function", [])




