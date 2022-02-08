from BitString import *
from Parameter import *
import math


class EvolutionaryAlgorithm:

    def __init__(self, name, description, parameters, algorithm):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.algorithm = algorithm

    # Update the min and max of the parameters if they depend on the size of the problem
    def update_parameters(self, size):
        for parameter in self.parameters:
            parameter.update_parameter(size)

    # Solve a fitness function with the algorithm and returns the number of iterations
    def solve(self, parameters, size, fitness_function, fitness_parameters):
        return self.algorithm(parameters, size, fitness_function, fitness_parameters)


# Algorithm for the (1+1) EA
def one_plus_one(parameters, size, fitness_function, fitness_parameters):
    strength = int(parameters[0])
    # Creation of a random bit string of length "size"
    bit_string = BitString(size)
    # Compute the value of the fitness function for the previously created bit string
    fitness_value = fitness_function.result(fitness_parameters, size, bit_string.string)
    iterations = 1
    # Compute the maximum of the function in order to know when this value is reached
    fitness_maximum = fitness_function.maximum(fitness_parameters, size)
    # found_maximum is true if the maximum has been reached
    found_maximum = (fitness_value == fitness_maximum)
    while not found_maximum:
        # Creation of the new bit string by flipping bits from the previous bit string
        new_bit_string = ""
        for bit in bit_string.string:
            if random.random() < strength/size:
                new_bit = str(1 - int(bit))
                new_bit_string += new_bit
            else:
                new_bit_string += bit
        new_fitness_value = fitness_function.result(fitness_parameters, size, new_bit_string)
        iterations += 1
        # If the fitness value of the new bit string is better than before, it is kept
        if new_fitness_value >= fitness_value:
            bit_string.string = new_bit_string
            fitness_value = new_fitness_value
            found_maximum = (fitness_value == fitness_maximum)
    return bit_string.string, iterations


# Algorithm for the SD(1+1) EA
def sd_one_plus_one(parameters, size, fitness_function, fitness_parameters):
    R = parameters[0]
    # Creation of a random bit string of length "size"
    bit_string = BitString(size)
    # Compute the value of the fitness function for the previously created bit string
    fitness_value = fitness_function.result(fitness_parameters, size, bit_string.string)
    iterations = 1
    # Compute the maximum of the function in order to know when this value is reached
    fitness_maximum = fitness_function.maximum(fitness_parameters, size)
    # found_maximum is true if the maximum has been reached
    found_maximum = (fitness_value == fitness_maximum)
    # Number of iteration with the actual strength
    u = 0
    # Strength
    r = 1
    while not found_maximum:
        # Creation of the new bit string by flipping bits from the previous bit string
        new_bit_string = ""
        for bit in bit_string.string:
            if random.random() < r/size:
                new_bit = str(1 - int(bit))
                new_bit_string += new_bit
            else:
                new_bit_string += bit
        new_fitness_value = fitness_function.result(fitness_parameters, size, new_bit_string)
        iterations += 1
        u = u + 1
        # If the fitness value of the new bit string is better than before, it is kept
        if new_fitness_value > fitness_value:
            bit_string.string = new_bit_string
            fitness_value = new_fitness_value
            found_maximum = (fitness_value == fitness_maximum)
            # The strength is reset to 1 and the number of iterations to 0
            r = 1
            u = 0
        # If the fitness value is equal to the previous one and the strength is 1, the new bit string is taken
        elif new_fitness_value == fitness_value and r == 1:
            bit_string.string = new_bit_string
            fitness_value = new_fitness_value
            found_maximum = (fitness_value == fitness_maximum)
        # After too many iterations, the strength is increased and the number of iterations reset to 0
        if u > 2 * pow(math.exp(1) * size / r, r) * math.log(size * int(R)):
            # TODO - Does this need to be rounded to the previous/next integer if size is odd ?
            r = min(r+1, size/2)
            u = 0

    return bit_string.string, iterations


# List containing every evolutionary algorithm
evolutionary_algorithms = []

# Creation of the (1+1) EA
# Strength -> Every bit if flipped with a probability of strength/size
Strength = Parameter("strength", "integer", 1, "size")
OnePlusOne = EvolutionaryAlgorithm("(1+1) EA", "(1+1) EA with static strength.", [Strength], one_plus_one)
evolutionary_algorithms.append(OnePlusOne)

# Creation of the SD(1+1) EA
# R -> it is used to control the probability of failing to find an improvement at the "right" strength
# R should be of the size of the image of the fitness function,
# If the image of the fitness function is unknown, R should have a value of at least the problem size
Param_R = Parameter("R", "integer", "size", float('inf'))
SDOnePlusOne = EvolutionaryAlgorithm("SD-(1+1) EA", "(1+1) EA with stagnation detection", [Param_R], sd_one_plus_one)
evolutionary_algorithms.append(SDOnePlusOne)



