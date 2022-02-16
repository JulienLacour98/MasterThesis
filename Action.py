from matplotlib import pyplot as plt

from EvolutionaryAlgorithm import *
from FitnessFunction import *
from utilities import *


class Action:

    def __init__(self, name, description,  parameters, algorithm):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.algorithm = algorithm
        actions.append(self)

    # Update the min and max of the parameters if they depend on the size of the problem
    def update_parameters(self, size):
        for parameter in self.parameters:
            parameter.update_parameter(size)


# Selection of a problem size i.e. number of bits per bit_string
def choose_problem_size():
    return choose_integer("Problem Size", 1, float('inf'))


# Selection of an evolutionary algorithm
def choose_evolutionary_algorithm(problem_size):
    return choose_element("Evolutionary Algorithm", evolutionary_algorithms, problem_size)


# Selection of a fitness function
def choose_fitness_function(problem_size):
    return choose_element("Fitness Function", fitness_functions, problem_size)


def display_fitness():
    problem_size = choose_problem_size()
    fitness_function, fitness_parameters = choose_fitness_function(problem_size)
    bit_string = BitString(problem_size)
    bit_string.only_zeros()
    x = np.empty(problem_size+1)
    y = np.empty(problem_size+1)
    x[0] = 0
    y[0] = fitness_function.result(fitness_parameters, problem_size, bit_string)
    for i in range(problem_size):
        bit_string.add_one_one()
        x[i+1] = i + 1
        y[i+1] = fitness_function.result(fitness_parameters, problem_size, bit_string)
    plt.title(fitness_function.name)
    plt.xlabel("|x|")
    plt.ylabel("f(x)")
    plt.plot(x, y, '.')
    plt.show()


def run_once():
    problem_size = choose_problem_size()
    evolutionary_algorithm, algorithm_parameters = choose_evolutionary_algorithm(problem_size)
    fitness_function, fitness_parameters = choose_fitness_function(problem_size)
    iterations, timer = evolutionary_algorithm.solve(algorithm_parameters, problem_size, fitness_function, fitness_parameters)
    print("")
    print("\nYou chose the following evolutionary algorithm: " + evolutionary_algorithm.name)
    print("The maximum of " + fitness_function.name
          + " for a problem size of " + str(problem_size)
          + " is: "
          + str(fitness_function.maximum(fitness_parameters, problem_size)))

    print("The algorithm ran in " + str(iterations) + " iterations and " + str(round(timer, 2)) + " seconds.")


def run_n_times():
    problem_size = choose_problem_size()
    evolutionary_algorithm, algorithm_parameters = choose_evolutionary_algorithm(problem_size)
    fitness_function, fitness_parameters = choose_fitness_function(problem_size)
    n = choose_integer("number of iterations", 1, float('inf'))
    results = np.empty(n)
    for i in range(n):
        results[i] = evolutionary_algorithm.solve(algorithm_parameters,
                                                  problem_size,
                                                  fitness_function,
                                                  fitness_parameters)
    print("")
    print("The mean of the number of iterations is: " + str(results.mean()))
    print("The minimum number of iterations is: " + str(results.min()))
    print("The maximum number of iterations is: " + str(results.max()))
    print("The median of the number of iterations is: " + str(np.median(results)))


actions = []

# Creation of Display Fitness
DisplayFitness = Action("DF", "Display graph of a fitness function", [], display_fitness, )

# Creation of Run Once
RunOnce = Action("R1", "Run evolutionary algorithm on one fitness function ", [], run_once, )

# Creation Run n Times
RunNTimes = Action("RN", "Run evolutionary algorithm n times on one fitness function", [], run_n_times, )




