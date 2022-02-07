from BitString import *


class EvolutionaryAlgorithm:

    def __init__(self, name, description, algorithm):
        self.name = name
        self.description = description
        self.algorithm = algorithm

    def solve(self, fitness_function):
        pass

    def solve_n_times(self, fitness_function, iterations):
        pass

    def statistical_results(self, fitness_function, iterations):
        pass


evolutionary_algorithms = []


def one_plus_one(strength, size, fitness_function):
    bit_string = BitString(size)
    fitness_value = fitness_function.result(bit_string.string)
    iterations = 1
    fitness_maximum = fitness_function.maximum(size)
    found_maximum = (fitness_value == fitness_maximum)
    while not found_maximum:
        new_bit_string = ""
        for bit in bit_string.string:
            if random.random() < strength/size:
                new_bit = str(1 - int(bit))
                new_bit_string += new_bit
            else:
                new_bit_string += bit
        new_fitness_value = fitness_function.result(new_bit_string)
        iterations += 1
        if new_fitness_value >= fitness_value:
            print(new_bit_string + ": " + str(new_fitness_value))
            bit_string.string = new_bit_string
            fitness_value = new_fitness_value
            found_maximum = (fitness_value == fitness_maximum)
    return iterations


OnePlusOne = EvolutionaryAlgorithm("(1+1) EA", "(1+1) EA with static strength r", one_plus_one)
evolutionary_algorithms.append(OnePlusOne)

