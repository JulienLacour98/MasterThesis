from EvolutionaryAlgorithm import *
from FitnessFunction import *

chosen_algorithm = False
while not chosen_algorithm:
    for i in range(1, len(evolutionary_algorithms) + 1):
        print(str(i) + ": " + evolutionary_algorithms[i-1].name)
    algorithm_index = input("Choose an evolutionary algorithm: ")
    if algorithm_index.isnumeric():
        algorithm_index = int(algorithm_index)
        if algorithm_index in range(1, len(evolutionary_algorithms) + 1):
            chosen_algorithm = True
            evolutionary_algorithm = evolutionary_algorithms[algorithm_index - 1]
        else:
            print("Your integer has to be between 1 and " + str(len(evolutionary_algorithms)))
    else:
        print("It has to be an integer")

chosen_fitness = False
while not chosen_fitness:
    for i in range(1, len(fitness_functions) + 1):
        print(str(i) + ": " + fitness_functions[i-1].name)
    fitness_index = input("Choose a fitness function: ")
    if fitness_index.isnumeric():
        fitness_index = int(fitness_index)
        if fitness_index in range(1, len(fitness_functions) + 1):
            chosen_fitness = True
            fitness_function = fitness_functions[fitness_index - 1]
        else:
            print("Your integer has to be between 1 and " + str(len(fitness_functions)))
    else:
        print("It has to be an integer")

chosen_size = False
while not chosen_size:
    problem_size = input("Choose the size of the problem: ")
    if problem_size.isnumeric():
        problem_size = int(problem_size)
        if problem_size > 0:
            chosen_size = True
        else:
            print("Your integer has to be greater than 0")
    else:
        print("It has to be an integer")

print("You chose the following evolutionary algorithm:" + evolutionary_algorithm.name)
print("The maximum of " + fitness_function.name +
      " for a problem size of " + str(problem_size) + " is: " + str(fitness_function.maximum(problem_size)))

print("The algorithm ran in "
      + str(evolutionary_algorithm.algorithm(1, problem_size, fitness_function))
      + " iterations")
