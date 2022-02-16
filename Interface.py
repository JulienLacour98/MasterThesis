from Action import *
from InterfaceUtilities import *


# Parent class for all the interfaces
class Interface(tk.Frame):

    def __init__(self, class_name, parent, controller):
        self.class_name = class_name
        self.parent = parent
        self.controller = controller


# Parent class for the different action interfaces
class ActionInterface(Interface):

    def __init__(self, class_name, parent, controller, action,
                 evolutionary_algorithm=evolutionary_algorithms[0],
                 fitness_function=fitness_functions[0]):

        super().__init__(class_name, parent, controller)
        self.action = action
        self.evolutionary_algorithm_name = StringVar()
        self.evolutionary_algorithm_name.set(evolutionary_algorithm.name)
        self.evolutionary_algorithm = evolutionary_algorithm
        self.evolutionary_parameters = evolutionary_algorithm.parameters
        self.evolutionary_parameter_values = []
        self.fitness_function_name = StringVar()
        self.fitness_function_name.set(fitness_function.name)
        self.fitness_function = fitness_function
        self.fitness_parameters = fitness_function.parameters
        self.fitness_parameter_values = []
        self.problem_size = IntVar()
        self.problem_size.set(100)

    def choice_of_evolutionary_algorithm(self, start_row):
        tk.Label(self, text="Choose an evolutionary algorithm: ").grid(row=start_row, column=0, padx=10, pady=10)
        choose_algorithm = OptionMenu(self,
                                      self.evolutionary_algorithm_name,
                                      *evolutionary_algorithm_names,
                                      command=self.change_evolutionary)
        choose_algorithm.grid(row=start_row, column=1, padx=10, pady=10)
        return start_row + 1

    def change_evolutionary(self, *args):
        new_frame = self.class_name(self.class_name, self.parent, self.controller, self.action,
                                    find_evolutionary(self.evolutionary_algorithm_name.get()),
                                    self.fitness_function)
        new_frame.grid(row=0, column=0, sticky="nsew")
        new_frame.tkraise()

    def choice_of_evolutionary_parameters(self, start_row):
        if len(self.evolutionary_parameters) == 0:
            return start_row
        else:
            tk.Label(self, text="Choose parameters for the evolutionary algorithm:")\
                .grid(row=start_row, column=0, padx=10, pady=10)
            for i in range(len(self.evolutionary_parameters)):
                evolutionary_parameter_value = tk.IntVar()
                evolutionary_parameter_value.set(self.evolutionary_parameters[i].default_value)
                tk.Label(self, text=self.evolutionary_parameters[i].name).grid(row=start_row+i, column=1, padx=10, pady=10)
                tk.Entry(self, justify=CENTER, textvariable=evolutionary_parameter_value)\
                    .grid(row=start_row+i, column=2, padx=10, pady=10)
                self.evolutionary_parameter_values.append(evolutionary_parameter_value)
            return start_row + len(self.evolutionary_parameters)

    def change_fitness(self, *args):
        new_frame = self.class_name(self.class_name, self.parent, self.controller, self.action,
                                    self.evolutionary_algorithm,
                                    find_fitness(self.fitness_function_name.get()))
        new_frame.grid(row=0, column=0, sticky="nsew")
        new_frame.tkraise()

    def choice_of_fitness_function(self, start_row):
        tk.Label(self, text="Choose a fitness function: ").grid(row=start_row, column=0, padx=10, pady=10)
        choose_fitness = OptionMenu(self,
                                    self.fitness_function_name,
                                    *fitness_function_names,
                                    command=self.change_fitness)
        choose_fitness.grid(row=start_row, column=1, padx=10, pady=10)
        return start_row + 1

    def choice_of_fitness_parameters(self, start_row):
        if len(self.fitness_parameters) == 0:
            return start_row
        else:
            tk.Label(self, text="Choose parameters for the fitness function:").grid(row=start_row, column=0, padx=10, pady=10)
            for i in range(len(self.fitness_parameters)):
                fitness_parameter_value = tk.IntVar()
                fitness_parameter_value.set(self.fitness_parameters[i].default_value)
                tk.Label(self, text=self.fitness_parameters[i].name).grid(row=start_row+i, column=1, padx=10, pady=10)
                tk.Entry(self, justify=CENTER, textvariable=fitness_parameter_value).grid(row=start_row+i, column=2, padx=10, pady=10)
                self.fitness_parameter_values.append(fitness_parameter_value)
            return start_row + len(self.fitness_parameters)

    def choice_of_problem_size(self, start_row):
        tk.Label(self, text="Problem Size:").grid(row=start_row, column=0, padx=10, pady=10)
        tk.Entry(self, justify=CENTER, textvariable=self.problem_size).grid(row=start_row, column=1, padx=10, pady=10)
        return start_row + 1


# Class for the main page interface
class StartPage(Interface):
    def __init__(self, class_name, parent, controller):
        super().__init__(class_name, parent, controller)

        # Creating of the frame
        frame_creation(self, "Main page")

        # Creating a button for each action leading to their interface
        tk.Label(self, text="Choose an action: ").grid(row=2, column=0, padx=10, pady=10)
        for i in range(len(actions)):
            ttk.Button(self, text=actions[i].description,
                       command=lambda i=i: controller.show_frame(globals()[actions[i].name]))\
                .grid(row=i+3, column=1, padx=10, pady=10)


# Interface for generating a graph of a fitness function
class DF(ActionInterface):

    def __init__(self, class_name, parent, controller, action,
                 evolutionary_algorithm=evolutionary_algorithms[0],
                 fitness_function=fitness_functions[0]):

        super().__init__(class_name, parent, controller, action, evolutionary_algorithm, fitness_function)

        frame_creation(self, "Display a fitness function", StartPage)
        row = self.choice_of_problem_size(2)
        row = self.choice_of_fitness_function(row)
        row = self.choice_of_fitness_parameters(row)

        # Create the graph of the fitness function
        display_button = ttk.Button(self, text="Display graph", command=lambda: self.display_fitness_graph(row+1))
        display_button.grid(row=row, column=2, padx=10, pady=10)

    def display_fitness_graph(self, start_row):
        # TODO - Check Constraints on every parameter
        problem_size = self.problem_size.get()
        fitness_parameter_values = []
        for fitness_parameter_value in self.fitness_parameter_values:
            fitness_parameter_values.append(fitness_parameter_value.get())
        bit_string = BitString(problem_size)
        bit_string.only_zeros()
        x = np.empty(problem_size + 1)
        y = np.empty(problem_size + 1)
        x[0] = 0
        y[0] = self.fitness_function.result(fitness_parameter_values, problem_size, bit_string)
        for i in range(problem_size):
            bit_string.add_one_one()
            x[i + 1] = i + 1
            y[i + 1] = self.fitness_function.result(fitness_parameter_values, problem_size, bit_string)
        build_graph(self, x, y, start_row, 2)


class R1(ActionInterface):

    def __init__(self, class_name, parent, controller, action,
                 evolutionary_algorithm=evolutionary_algorithms[0],
                 fitness_function=fitness_functions[0]):

        super().__init__(class_name, parent, controller, action, evolutionary_algorithm, fitness_function)

        frame_creation(self, "Run an evolutionary algorithm on a fitness function", StartPage)
        row = self.choice_of_problem_size(2)
        row = self.choice_of_evolutionary_algorithm(row)
        row = self.choice_of_evolutionary_parameters(row)
        row = self.choice_of_fitness_function(row)
        row = self.choice_of_fitness_parameters(row)

        # Create the graph of the fitness function
        display_button = ttk.Button(self, text="Solve", command=lambda: self.solve(row+1))
        display_button.grid(row=row, column=2, padx=10, pady=10)

    def solve(self, start_row):
        problem_size = self.problem_size.get()
        evolutionary_parameter_values = []
        for evolutionary_parameter_value in self.evolutionary_parameter_values:
            evolutionary_parameter_values.append(evolutionary_parameter_value.get())
        fitness_parameter_values = []
        for fitness_parameter_value in self.fitness_parameter_values:
            fitness_parameter_values.append(fitness_parameter_value.get())
        bit_string, iterations, timer = self.evolutionary_algorithm.solve(evolutionary_parameter_values,
                                                                          problem_size,
                                                                          self.fitness_function,
                                                                          fitness_parameter_values)
        tk.Label(self, text="The solution was found in " + str(timer) + " seconds")\
            .grid(row=start_row, column=1, padx=10, pady=10)
        tk.Label(self, text="The solution was found in " + str(iterations) + " iterations")\
            .grid(row=start_row+1, column=1, padx=10, pady=10)


class RN(ActionInterface):

    def __init__(self, class_name, parent, controller, action,
                 evolutionary_algorithm=evolutionary_algorithms[0],
                 fitness_function=fitness_functions[0]):

        super().__init__(class_name, parent, controller, action, evolutionary_algorithm, fitness_function)

        frame_creation(self, "Run an evolutionary algorithm n times on a fitness function", StartPage)
