from EvolutionaryAlgorithm import *
from FitnessFunction import *
from matplotlib import pyplot as plt


class Actions:

    def __init__(self, name, parameters, algorithm):
        self.name = name
        self.parameters = parameters
        self.algorithm = algorithm


# Selection of a problem size i.e. number of bits per bit_string
def choose_problem_size():
    chosen_size = False
    while not chosen_size:
        problem_size = input("Choose the size of the problem: ")
        # Checking that the number is an integer
        if problem_size.isnumeric():
            problem_size = int(problem_size)
            # Checking that the integer is not 0
            if problem_size > 0:
                chosen_size = True
            else:
                print("Your integer has to be greater than 0")
        else:
            print("It has to be an integer")
    return problem_size


# Selection of an evolutionary algorithm
def choose_evolutionary_algorithm(problem_size):
    # Output the different evolutionary algorithms and updating min and max values of the parameters
    print("Evolutionary Algorithms: ")
    for i in range(len(evolutionary_algorithms)):
        evolutionary_algorithms[i].update_parameters(problem_size)
        print("    - " + str(i + 1) + ": " + evolutionary_algorithms[i].name)
    chosen_algorithm = False
    while not chosen_algorithm:
        algorithm_index = input("Choose an evolutionary algorithm: ")
        # Checking that the number is an integer
        if algorithm_index.isnumeric():
            algorithm_index = int(algorithm_index) - 1
            # Checking that the integer is the index of one of the algorithms
            if algorithm_index in range(len(evolutionary_algorithms)):
                chosen_algorithm = True
                evolutionary_algorithm = evolutionary_algorithms[algorithm_index]
                # Selection of the value of the parameters
                algorithm_parameters = []
                for parameter in evolutionary_algorithm.parameters:
                    chosen_parameter = False
                    while not chosen_parameter:
                        input_parameter = input("Enter parameter " + parameter.name + " of the algorithm: ")
                        # Checking that the value of the parameter is valid
                        if parameter.is_value_valid(input_parameter):
                            algorithm_parameters.append(input_parameter)
                            chosen_parameter = True
            else:
                print("Your integer has to be between 1 and " + str(len(evolutionary_algorithms)))
        else:
            print("It has to be an integer")
    return evolutionary_algorithm, algorithm_parameters


# Selection of a fitness function
def choose_fitness_function(problem_size):
    # Output the different fitness functions and updating min and max values of the parameters
    print("\nFitness Functions:")
    for i in range(len(fitness_functions)):
        print("    - " + str(i+1) + ": " + fitness_functions[i].name)
        fitness_functions[i].update_parameters(problem_size)
    chosen_fitness = False
    while not chosen_fitness:
        fitness_index = input("Choose a fitness function: ")
        # Checking that the number is an integer
        if fitness_index.isnumeric():
            fitness_index = int(fitness_index) - 1
            # Checking that the integer is the index of one of the functions
            if fitness_index in range(len(fitness_functions)):
                chosen_fitness = True
                fitness_function = fitness_functions[fitness_index]
                # Selection of the value of the parameters
                fitness_parameters = []
                for parameter in fitness_function.parameters:
                    chosen_parameter = False
                    while not chosen_parameter:
                        input_parameter = input("Enter parameter " + parameter.name + " of the fitness function: ")
                        # Checking that the value of the parameter is valid
                        if parameter.is_value_valid(input_parameter):
                            fitness_parameters.append(input_parameter)
                            chosen_parameter = True
            else:
                print("Your integer has to be between 1 and " + str(len(fitness_functions)))
        else:
            print("It has to be an integer")
    return fitness_function, fitness_parameters


def run_once():
    problem_size = choose_problem_size()
    evolutionary_algorithm, algorithm_parameters = choose_evolutionary_algorithm(problem_size)
    fitness_function, fitness_parameters = choose_fitness_function(problem_size)

    print("\nYou chose the following evolutionary algorithm: " + evolutionary_algorithm.name)
    print("The maximum of " + fitness_function.name
          + " for a problem size of " + str(problem_size)
          + " is: "
          + str(fitness_function.maximum(fitness_parameters, problem_size)))

    print("The algorithm ran in "
          + str(evolutionary_algorithm.solve(algorithm_parameters, problem_size, fitness_function, fitness_parameters))
          + " iterations.")


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


actions = []

# Creation of RunOnce
RunOnce = Actions("Run once", [], run_once)
actions.append(RunOnce)

# Creation of DisplayFitness
DisplayFitness = Actions("Display fitness function", [], display_fitness)
actions.append(DisplayFitness)




