from BitString import *
from Parameter import *
import math
import numpy as np
import time


class EvolutionaryAlgorithm:

    def __init__(self, name, parameters, algorithm):
        self.name = name
        self.parameters = parameters
        self.algorithm = algorithm
        evolutionary_algorithms.append(self)
        evolutionary_algorithm_names.append(self.name)

    # Update the min and max of the parameters if they depend on the size of the problem
    def update_parameters(self, size):
        for parameter in self.parameters:
            parameter.update_parameter(size)

    # Solve a fitness function with the algorithm and returns the number of iterations
    def solve(self, evolutionary_parameters, size, fitness_function, fitness_parameters):
        t1 = time.time()
        bit_string, iterations, x, y = self.algorithm(evolutionary_parameters, size, fitness_function, fitness_parameters)
        t2 = time.time()
        return bit_string.string, iterations, t2 - t1, x, y


# Algorithm for the (1+1) EA
def one_plus_one(parameters, size, fitness_function, fitness_parameters):
    strength = parameters[0]
    # Creation of a random bit string of length "size"
    bit_string = BitString(size)
    # Compute the value of the fitness function for the previously created bit string
    fitness_value = fitness_function.result(fitness_parameters, size, bit_string)
    iterations = 1
    x = [1]
    y = [fitness_value]
    # Compute the maximum of the function in order to know when this value is reached
    fitness_maximum = fitness_function.maximum(fitness_parameters, size)
    # found_maximum is true if the maximum has been reached
    found_maximum = (fitness_value == fitness_maximum)
    while not found_maximum:
        # Creation of the offspring
        new_bit_string = bit_string.create_offspring_p(strength/size)
        new_fitness_value = fitness_function.result(fitness_parameters, size, new_bit_string)
        iterations += 1
        # If the fitness value of the new bit string is better than before, it is kept
        if new_fitness_value >= fitness_value:
            bit_string = new_bit_string
            fitness_value = new_fitness_value
            found_maximum = (fitness_value == fitness_maximum)
            x.append(iterations)
            y.append(fitness_value)
    return bit_string, iterations, x, y


# Algorithm for the SD(1+1) EA
def sd_one_plus_one(parameters, size, fitness_function, fitness_parameters):
    R = parameters[0]
    # Creation of a random bit string of length "size"
    bit_string = BitString(size)
    # Compute the value of the fitness function for the previously created bit string
    fitness_value = fitness_function.result(fitness_parameters, size, bit_string)
    iterations = 1
    x = [1]
    y = [fitness_value]
    # Compute the maximum of the function in order to know when this value is reached
    fitness_maximum = fitness_function.maximum(fitness_parameters, size)
    # found_maximum is true if the maximum has been reached
    found_maximum = (fitness_value == fitness_maximum)
    # Number of iteration with the actual strength
    u = 0
    # Strength
    r = 1
    while not found_maximum:
        # Creation of the offspring
        new_bit_string = bit_string.create_offspring_p(r/size)
        new_fitness_value = fitness_function.result(fitness_parameters, size, new_bit_string)
        iterations += 1
        u = u + 1
        # If the fitness value of the new bit string is better than before, it is kept
        if new_fitness_value > fitness_value:
            bit_string = new_bit_string
            fitness_value = new_fitness_value
            found_maximum = (fitness_value == fitness_maximum)
            x.append(iterations)
            y.append(fitness_value)
            # The strength is reset to 1 and the number of iterations to 0
            new_r = 1
            u = 0
        # If the fitness value is equal to the previous one and the strength is 1, the new bit string is taken
        elif new_fitness_value == fitness_value and r == 1:
            bit_string = new_bit_string
            fitness_value = new_fitness_value
            found_maximum = (fitness_value == fitness_maximum)
            x.append(iterations)
            y.append(fitness_value)
        # After too many iterations, the strength is increased and the number of iterations reset to 0
        if u > 2 * pow(math.exp(1) * size / r, r) * math.log(size * R):
            # TODO - Does this need to be rounded to the previous/next integer if size is odd ?
            new_r = min(r+1, size/2)
            u = 0
        else:
            new_r = r
        r = new_r
    return bit_string, iterations, x, y


def sasd_one_plus_lambda(parameters, size, fitness_function, fitness_parameters):
    R = parameters[0]
    r_init = parameters[1]
    lbd = parameters[2]
    # Creation of a random bit string of length "size"
    bit_string = BitString(size)
    # Compute the value of the fitness function for the previously created bit string
    fitness_value = fitness_function.result(fitness_parameters, size, bit_string)
    iterations = 1
    x = [1]
    y = [fitness_value]
    # Compute the maximum of the function in order to know when this value is reached
    fitness_maximum = fitness_function.maximum(fitness_parameters, size)
    # found_maximum is true if the maximum has been reached
    found_maximum = (fitness_value == fitness_maximum)
    # Number of iteration with the actual strength
    u = 0
    # Strength
    r = r_init
    # Boolean variable indication stagnation detection
    g = False
    while not found_maximum:
        u = u + 1
        if g:
            # Creation of lambda offsprings
            new_bit_strings = []
            new_fitness_values = []
            for i in range(lbd):
                new_bit_string = bit_string.create_offspring_p(r/size)
                new_bit_strings.append(new_bit_string)
                new_fitness_values.append(fitness_function.result(fitness_parameters, size, new_bit_string))
                iterations += 1
            max_index = np.argmax(new_fitness_values)
            new_bit_string = new_bit_strings[max_index]
            new_fitness_value = new_fitness_values[max_index]
            # If the fitness value of the best new bit string is better than before, it is kept
            if new_fitness_value > fitness_value:
                bit_string = new_bit_string
                fitness_value = new_fitness_value
                found_maximum = (fitness_value == fitness_maximum)
                x.append(iterations)
                y.append(fitness_value)
                new_r = r_init
                g = False
                u = 0
            else:
                if u > 2 * pow(math.exp(1) * size / r, r) * math.log(size * int(R)) / lbd:
                    new_r = min(r + 1, size/2)
                    u = 0
                else:
                    new_r = r
        # g = False
        else:
            # Creation of lambda offsprings
            new_bit_strings = []
            new_fitness_values = []
            for i in range(lbd):
                if i <= lbd / 2:
                    p = r / (2 * size)
                else:
                    p = 2 * r / size
                new_bit_string = bit_string.create_offspring_p(p)
                new_bit_strings.append(new_bit_string)
                new_fitness_values.append(fitness_function.result(fitness_parameters, size, new_bit_string))
                iterations += 1
            max_index = np.argmax(new_fitness_values)
            new_bit_string = new_bit_strings[max_index]
            new_fitness_value = new_fitness_values[max_index]
            # If the fitness value of the best new bit string is better than before, it is kept
            if new_fitness_value >= fitness_value:
                if new_fitness_value > fitness_value:
                    u = 0
                bit_string = new_bit_string
                fitness_value = new_fitness_value
                found_maximum = (fitness_value == fitness_maximum)
                x.append(iterations)
                y.append(fitness_value)
            if random.random() < 1/2:
                # TODO - Is this correct ?
                r = r
            else:
                if random.random() < 1/2:
                    r = r/2
                else:
                    r = 2*r
            new_r = min(max(2, r), size/4)
            # TODO - Fix because values can become too large
            if u > 2 * pow(math.exp(1) * size / r, r) * math.log(size * R) / lbd:
                new_r = 2
                g = True
                u = 0
        r = new_r
    return bit_string, iterations, x, y


def sd_rls_r(parameters, size, fitness_function, fitness_parameters):
    R = parameters[0]
    bit_string = BitString(size)
    fitness_value = fitness_function.result(fitness_parameters, size, bit_string)
    iterations = 1
    x = [1]
    y = [fitness_value]
    fitness_maximum = fitness_function.maximum(fitness_parameters, size)
    found_maximum = (fitness_value == fitness_maximum)
    r = 1
    s = 1
    u = 0
    while not found_maximum:
        new_bit_string = bit_string.create_offspring_s(s)
        new_fitness_value = fitness_function.result(fitness_parameters, size, new_bit_string)
        iterations += 1
        u += 1
        if new_fitness_value > fitness_value:
            bit_string = new_bit_string
            fitness_value = new_fitness_value
            found_maximum = (fitness_value == fitness_maximum)
            x.append(iterations)
            y.append(fitness_value)
            r = 1
            s = 1
            u = 0
        elif new_fitness_value == fitness_value and r == 1:
            bit_string = new_bit_string
            fitness_value = new_fitness_value
            found_maximum = (fitness_value == fitness_maximum)
            x.append(iterations)
            y.append(fitness_value)
        if u > math.comb(size, s) * math.log(R):
            if s == 1:
                if r < size/2:
                    r += 1
                else:
                    r = size
                s = r
            else:
                s += -1
            u = 0
    return bit_string, iterations, x, y


def sd_rls_m(parameters, size, fitness_function, fitness_parameters):
    R = parameters[0]
    bit_string = BitString(size)
    fitness_value = fitness_function.result(fitness_parameters, size, bit_string)
    iterations = 1
    x = [1]
    y = [fitness_value]
    fitness_maximum = fitness_function.maximum(fitness_parameters, size)
    found_maximum = (fitness_value == fitness_maximum)
    r = 1
    s = 1
    u = 0
    B = float('inf')
    while not found_maximum:
        new_bit_string = bit_string.create_offspring_s(s)
        new_fitness_value = fitness_function.result(fitness_parameters, size, new_bit_string)
        iterations += 1
        u += 1
        if new_fitness_value > fitness_value:
            bit_string = new_bit_string
            fitness_value = new_fitness_value
            found_maximum = (fitness_value == fitness_maximum)
            x.append(iterations)
            y.append(fitness_value)
            r = s
            s = 1
            if r > 1:
                B = u / (math.log(size) * (r-1))
            else:
                B = float('inf')
            u = 0
        elif new_fitness_value == fitness_value and r == 1:
            bit_string = new_bit_string
            fitness_value = new_fitness_value
            found_maximum = (fitness_value == fitness_maximum)
            x.append(iterations)
            y.append(fitness_value)
        if u > min(B, math.comb(size, s) * math.log(R)):
            if s == r:
                if r < size/2:
                    r += 1
                else:
                    r = size
                s = 1
            else:
                s += 1
                if s == r:
                    B = float('inf')
                u = 0
    return bit_string, iterations, x, y


# TODO- Update default values

# List containing every evolutionary algorithm
evolutionary_algorithms = []
evolutionary_algorithm_names = []

# Creation of the (1+1) EA
# Strength -> Every bit if flipped with a probability of strength/size
Strength = Parameter("Strength", "integer", 1, 1, "size", [])
OnePlusOne = EvolutionaryAlgorithm("(1+1) EA", [Strength], one_plus_one)
evolutionary_algorithms.append(OnePlusOne)

# Creation of the SD(1+1) EA
# R -> it is used to control the probability of failing to find an improvement at the "right" strength
# R should be of the size of the image of the fitness function,
# If the image of the fitness function is unknown, R should have a value of at least the problem size
paramR = Parameter("R", "integer", 100, "size", float('inf'), [])
SDOnePlusOne = EvolutionaryAlgorithm("SD-(1+1) EA", [paramR], sd_one_plus_one)
evolutionary_algorithms.append(SDOnePlusOne)

# Creation of the SASD-(1+lambda) EA
# Lambda -> Number of offsprings created from the parent
paramR = Parameter("R", "integer", 100, "size", float('inf'), [])
Initial_Strength = Parameter("Initial strength", "integer", 1, 1, "size", [])
Lambda = Parameter("Lambda", "integer", 10, 1, float('inf'), [])
SASDOnePlusLambda = EvolutionaryAlgorithm("SASD-(1+lambda) EA", [paramR, Initial_Strength, Lambda], sasd_one_plus_lambda)
evolutionary_algorithms.append(SASDOnePlusLambda)

# Creation of the SD-RLS_r
paramR = Parameter("R", "integer", 100,  "size", float('inf'), [])
SDRLSR = EvolutionaryAlgorithm("SD-RLS_r", [paramR], sd_rls_r)
evolutionary_algorithms.append(SDRLSR)

# Creation of the SD-RLS_m
paramR = Parameter("R", "integer", 100, "size", float('inf'), [])
SDRLSM = EvolutionaryAlgorithm("SD-RLS_m", [paramR], sd_rls_m)
evolutionary_algorithms.append(SDRLSM)




