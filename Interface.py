# TODO - Clean how the classes are created -> try to remove useless attributes from main classes

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
                 problem_size, problem_size_end, step, iterations,
                 fitness_function, fitness_parameter_values,
                 evolutionary_algorithm, evolutionary_parameter_values,
                 labels, xs, ys):

        super().__init__(class_name, parent, controller)
        self.action = action
        self.fitness_function_name = StringVar()
        self.fitness_function_name.set(fitness_function.name)
        self.fitness_function = fitness_function
        self.fitness_parameters = fitness_function.parameters
        self.fitness_parameter_values = fitness_parameter_values
        self.evolutionary_algorithm_name = StringVar()
        self.evolutionary_algorithm_name.set(evolutionary_algorithm.name)
        self.evolutionary_algorithm = evolutionary_algorithm
        self.evolutionary_parameters = evolutionary_algorithm.parameters
        self.evolutionary_parameter_values = evolutionary_parameter_values
        self.problem_size = problem_size
        self.problem_size_end = problem_size_end
        self.step = step
        self.iterations = iterations
        self.labels = labels
        self.xs = xs
        self.ys = ys

        frame_creation(self, action.description, StartPage)

    def choice_of_problem_size(self, start_row):
        tk.Label(self, text="Problem Size:").grid(row=start_row, column=0, padx=5, pady=5)
        tk.Entry(self, justify=CENTER, textvariable=self.problem_size).grid(row=start_row, column=1, padx=5, pady=5)
        return start_row + 1

    def choice_of_problem_range(self, start_row):
        tk.Label(self, text="Problem Size from").grid(row=start_row, column=0, padx=5, pady=5)
        tk.Entry(self, justify=CENTER, textvariable=self.problem_size).grid(row=start_row, column=1, padx=5, pady=5)
        tk.Label(self, text="to").grid(row=start_row, column=2, padx=5, pady=5)
        tk.Entry(self, justify=CENTER, textvariable=self.problem_size_end).grid(row=start_row, column=3, padx=5, pady=5)
        tk.Label(self, text="Step").grid(row=start_row+1, column=0, padx=5, pady=5)
        tk.Entry(self, justify=CENTER, textvariable=self.step).grid(row=start_row+1, column=1, padx=5, pady=5)
        return start_row + 2

    def choice_of_number_of_iterations(self, start_row):
        tk.Label(self, text="Number of iterations:").grid(row=start_row, column=0, padx=5, pady=5)
        tk.Entry(self, justify=CENTER, textvariable=self.iterations).grid(row=start_row, column=1, padx=5, pady=5)
        return start_row + 1

    def change_fitness(self, *args):
        fitness_function = find_fitness(self.fitness_function_name.get())
        new_frame = self.class_name(self.class_name, self.parent, self.controller, self.action,
                                    self.problem_size, self.problem_size_end, self.step, self.iterations,
                                    fitness_function, default_parameters(fitness_function, self.problem_size.get()),
                                    self.evolutionary_algorithm, self.evolutionary_parameter_values,
                                    [], [], [])
        new_frame.grid(row=0, column=0, sticky="nsew")
        new_frame.tkraise()

    def choice_of_fitness_function(self, start_row):
        tk.Label(self, text="Choose a fitness function: ").grid(row=start_row, column=0, padx=5, pady=5)
        choose_fitness = OptionMenu(self,
                                    self.fitness_function_name,
                                    *fitness_function_names,
                                    command=self.change_fitness)
        choose_fitness.grid(row=start_row, column=1, padx=5, pady=5)
        return start_row + 1

    def choice_of_fitness_parameters(self, start_row):
        if len(self.fitness_parameters) == 0:
            return start_row
        else:
            tk.Label(self, text="Choose parameters for the fitness function:")\
                .grid(row=start_row, column=0, padx=5, pady=5)
            for i in range(len(self.fitness_parameters)):
                tk.Label(self, text=self.fitness_parameters[i].name).grid(row=start_row+i, column=1, padx=5, pady=5)
                tk.Entry(self, justify=CENTER, textvariable=self.fitness_parameter_values[i])\
                    .grid(row=start_row+i, column=2, padx=5, pady=5)
            return start_row + len(self.fitness_parameters)

    def change_evolutionary(self, *args):
        evolutionary_algorithm = find_evolutionary(self.evolutionary_algorithm_name.get())
        new_frame = self.class_name(self.class_name, self.parent, self.controller, self.action,
                                    self.problem_size, self.problem_size_end, self.step, self.iterations,
                                    self.fitness_function, self.fitness_parameter_values,
                                    evolutionary_algorithm,
                                    default_parameters(evolutionary_algorithm, self.problem_size.get()),
                                    self.labels, self.xs, self.ys)
        new_frame.grid(row=0, column=0, sticky="nsew")
        new_frame.tkraise()

    def choice_of_evolutionary_algorithm(self, start_row):
        tk.Label(self, text="Choose an evolutionary algorithm: ").grid(row=start_row, column=0, padx=5, pady=5)
        choose_algorithm = OptionMenu(self,
                                      self.evolutionary_algorithm_name,
                                      *evolutionary_algorithm_names,
                                      command=self.change_evolutionary)
        choose_algorithm.grid(row=start_row, column=1, padx=5, pady=5)
        return start_row + 1

    def choice_of_evolutionary_parameters(self, start_row):
        if len(self.evolutionary_parameters) == 0:
            return start_row
        else:
            tk.Label(self, text="Choose parameters for the evolutionary algorithm:")\
                .grid(row=start_row, column=0, padx=5, pady=5)
            for i in range(len(self.evolutionary_parameters)):
                tk.Label(self, text=self.evolutionary_parameters[i].name)\
                    .grid(row=start_row+i, column=1, padx=5, pady=5)
                tk.Entry(self, justify=CENTER, textvariable=self.evolutionary_parameter_values[i])\
                    .grid(row=start_row+i, column=2, padx=5, pady=5)
            return start_row + len(self.evolutionary_parameters)

    def check_size(self, size_row, size_column):
        valid = True
        size_constraint = self.fitness_function.size_constraint
        for label in self.grid_slaves(size_row, size_column):
            label.grid_forget()
        if not size_constraint.check_condition(self.problem_size.get()):
            tk.Label(self, text=size_constraint.description).grid(row=size_row, column=size_column, padx=5, pady=5)
            valid = False
        return valid

    def check_fitness_parameters(self, fitness_row, fitness_column):
        valid = True
        fitness_parameters = self.fitness_function.parameters
        for i in range(len(fitness_parameters)):
            for label in self.grid_slaves(fitness_row + i, fitness_column):
                label.grid_forget()
            correctness = fitness_parameters[i].is_value_valid(self.fitness_parameter_values[i].get(),
                                                               self.problem_size.get())
            if correctness != "correct":
                tk.Label(self, text=correctness).grid(row=fitness_row + i, column=fitness_column, padx=5, pady=5)
                valid = False
        return valid

    def check_evolutionary_parameters(self, evolutionary_row, evolutionary_column):
        valid = True
        evolutionary_parameters = self.evolutionary_algorithm.parameters
        for i in range(len(evolutionary_parameters)):
            for label in self.grid_slaves(evolutionary_row + i, evolutionary_column):
                label.grid_forget()
            correctness = evolutionary_parameters[i].is_value_valid(self.evolutionary_parameter_values[i].get(),
                                                                    self.problem_size.get())
            if correctness != "correct":
                tk.Label(self, text=correctness)\
                    .grid(row=evolutionary_row + i, column=evolutionary_column, padx=5, pady=5)
                valid = False
        return valid


# Class for the main page interface
class StartPage(Interface):
    def __init__(self, class_name, parent, controller):
        super().__init__(class_name, parent, controller)

        # Creating of the frame
        frame_creation(self, "Main page")

        # Creating a button for each action leading to their interface
        tk.Label(self, text="Choose an action: ").grid(row=2, column=0, padx=5, pady=5)
        for i in range(len(actions)):
            ttk.Button(self, text=actions[i].description,
                       command=lambda i=i: controller.show_frame(globals()[actions[i].name]))\
                .grid(row=i+3, column=1, padx=5, pady=5)


# Interface for generating a graph of a fitness function
class DF(ActionInterface):

    def __init__(self, class_name, parent, controller, action,
                 problem_size, problem_size_end, step, iterations,
                 fitness_function, fitness_parameter_values,
                 evolutionary_algorithm, evolutionary_parameter_values, labels, xs, ys):

        super().__init__(class_name, parent, controller, action,
                         problem_size, problem_size_end, step, iterations,
                         fitness_function, fitness_parameter_values,
                         evolutionary_algorithm, evolutionary_parameter_values, labels, xs, ys)

        row = self.choice_of_problem_size(2)
        fitness_row = self.choice_of_fitness_function(row)
        row = self.choice_of_fitness_parameters(fitness_row)

        # Create the graph of the fitness function
        display_button = ttk.Button(self, text="Display graph",
                                    command=lambda: self.display_fitness_graph(row+1, 2, 2, fitness_row, 3))
        display_button.grid(row=row, column=2, padx=5, pady=5)

    def display_fitness_graph(self, start_row, size_row, size_column, fitness_row, fitness_column):
        problem_size = self.problem_size.get()
        if self.check_size(size_row, size_column) and self.check_fitness_parameters(fitness_row, fitness_column):
            fitness_parameter_values = []
            for fitness_parameter_value in self.fitness_parameter_values:
                fitness_parameter_values.append(fitness_parameter_value.get())
            bit_string = only_zeros(problem_size)
            x = np.empty(problem_size + 1)
            y = np.empty(problem_size + 1)
            x[0] = 0
            y[0] = self.fitness_function.result(fitness_parameter_values, problem_size, bit_string)
            for i in range(problem_size):
                bit_string.add_one_one()
                x[i + 1] = i + 1
                y[i + 1] = self.fitness_function.result(fitness_parameter_values, problem_size, bit_string)
            build_graph(self, [self.fitness_function_name.get()], [x], [y], start_row, 2, self.fitness_function.name +
                        " as a function of the norm", '|x|', 'f(x)')


class R1(ActionInterface):

    def __init__(self, class_name, parent, controller, action,
                 problem_size, problem_size_end, step, iterations,
                 fitness_function, fitness_parameter_values,
                 evolutionary_algorithm, evolutionary_parameter_values, labels, xs, ys):

        super().__init__(class_name, parent, controller, action,
                         problem_size, problem_size_end, step, iterations,
                         fitness_function, fitness_parameter_values,
                         evolutionary_algorithm, evolutionary_parameter_values, labels, xs, ys)

        row = self.choice_of_problem_size(2)
        fitness_row = self.choice_of_fitness_function(row)
        row = self.choice_of_fitness_parameters(fitness_row)
        evolutionary_row = self.choice_of_evolutionary_algorithm(row)
        row = self.choice_of_evolutionary_parameters(evolutionary_row)

        # Solve the problem and display results
        display_button = ttk.Button(self, text="Run", command=lambda: self.solve(row+1, 2, 2,
                                                                                 fitness_row, 3, evolutionary_row, 3))
        display_button.grid(row=row, column=2, padx=5, pady=5)

    def solve(self, start_row, size_row, size_column,
              fitness_row, fitness_column,
              evolutionary_row, evolutionary_column):
        if self.check_size(size_row, size_column) and \
                self.check_fitness_parameters(fitness_row, fitness_column) and \
                self.check_evolutionary_parameters(evolutionary_row, evolutionary_column):
            problem_size = self.problem_size.get()
            fitness_parameter_values = []
            for fitness_parameter_value in self.fitness_parameter_values:
                fitness_parameter_values.append(fitness_parameter_value.get())
            evolutionary_parameter_values = []
            for evolutionary_parameter_value in self.evolutionary_parameter_values:
                evolutionary_parameter_values.append(evolutionary_parameter_value.get())

            bit_string, iterations, timer, x, y = self.evolutionary_algorithm.solve(evolutionary_parameter_values,
                                                                                    problem_size,
                                                                                    self.fitness_function,
                                                                                    fitness_parameter_values)
            tk.Label(self, text="The solution was found in " + str(round(timer, 2)) + " seconds")\
                .grid(row=start_row, column=1, padx=5, pady=5)
            tk.Label(self, text="The solution was found in " + str(iterations) + " iterations")\
                .grid(row=start_row+1, column=1, padx=5, pady=5)

            build_graph(self, [self.evolutionary_algorithm.name],  [x], [y], start_row+2, 1, "Improvements of the bit string", 'iterations', 'f(x)')


class RN(ActionInterface):

    def __init__(self, class_name, parent, controller, action,
                 problem_size, problem_size_end, step, iterations,
                 fitness_function, fitness_parameter_values,
                 evolutionary_algorithm, evolutionary_parameter_values, labels, xs, ys):

        super().__init__(class_name, parent, controller, action,
                         problem_size, problem_size_end, step, iterations,
                         fitness_function, fitness_parameter_values,
                         evolutionary_algorithm, evolutionary_parameter_values, labels, xs, ys)

        row = self.choice_of_problem_size(2)
        row = self.choice_of_number_of_iterations(row)
        fitness_row = self.choice_of_fitness_function(row)
        row = self.choice_of_fitness_parameters(fitness_row)
        evolutionary_row = self.choice_of_evolutionary_algorithm(row)
        row = self.choice_of_evolutionary_parameters(evolutionary_row)

        # Create the graph of the fitness function
        display_button = ttk.Button(self, text="Run", command=lambda: self.solve_n_times(row+1, 2, 2,
                                                                                         fitness_row, 3,
                                                                                         evolutionary_row, 3))
        display_button.grid(row=row, column=2, padx=5, pady=5)

    def solve_n_times(self, start_row, size_row, size_column,
                      fitness_row, fitness_column, evolutionary_row, evolutionary_column):
        if self.check_size(size_row, size_column) and \
                self.check_fitness_parameters(fitness_row, fitness_column) and \
                self.check_evolutionary_parameters(evolutionary_row, evolutionary_column):
            problem_size = self.problem_size.get()
            iterations = self.iterations.get()
            fitness_parameter_values = []
            for fitness_parameter_value in self.fitness_parameter_values:
                fitness_parameter_values.append(fitness_parameter_value.get())
            evolutionary_parameter_values = []
            for evolutionary_parameter_value in self.evolutionary_parameter_values:
                evolutionary_parameter_values.append(evolutionary_parameter_value.get())
            results = np.empty(iterations)
            for i in range(iterations):
                _, results[i], _, _, _ = self.evolutionary_algorithm.solve(evolutionary_parameter_values,
                                                                           problem_size,
                                                                           self.fitness_function,
                                                                           fitness_parameter_values)

            tk.Label(self, text="The minimum number of iterations is: " + str(int(results.min()))) \
                .grid(row=start_row , column=1, padx=5, pady=5)
            tk.Label(self, text="The maximum number of iterations is: " + str(int(results.max()))) \
                .grid(row=start_row + 1, column=1, padx=5, pady=5)
            tk.Label(self, text="The mean of the number of iterations is: " + str(round(results.mean(), 2))) \
                .grid(row=start_row + 2, column=1, padx=5, pady=5)
            tk.Label(self, text="The median of the number of iterations is: " + str(int(np.median(results)))) \
                .grid(row=start_row + 3, column=1, padx=5, pady=5)


class RNM(ActionInterface):

    def __init__(self, class_name, parent, controller, action,
                 problem_size, problem_size_end, step, iterations,
                 fitness_function, fitness_parameter_values,
                 evolutionary_algorithm, evolutionary_parameter_values, labels, xs, ys):

        super().__init__(class_name, parent, controller, action,
                         problem_size, problem_size_end, step, iterations,
                         fitness_function, fitness_parameter_values,
                         evolutionary_algorithm, evolutionary_parameter_values, labels, xs, ys)

        row = self.choice_of_problem_range(2)
        row = self.choice_of_number_of_iterations(row)
        fitness_row = self.choice_of_fitness_function(row)
        row = self.choice_of_fitness_parameters(fitness_row)
        evolutionary_row = self.choice_of_evolutionary_algorithm(row)
        row = self.choice_of_evolutionary_parameters(evolutionary_row)

        # Create the graph of the fitness function
        display_button = ttk.Button(self, text="Run", command=lambda: self.solve_n_m_times(row+1))
        display_button.grid(row=row, column=2, padx=5, pady=5)

# TODO - Add the constraints
    def solve_n_m_times(self, start_row):
        problem_size = self.problem_size.get()
        problem_size_end = self.problem_size_end.get()
        step = self.step.get()

        iterations = self.iterations.get()
        fitness_parameter_values = []
        for fitness_parameter_value in self.fitness_parameter_values:
            fitness_parameter_values.append(fitness_parameter_value.get())
        evolutionary_parameter_values = []
        for evolutionary_parameter_value in self.evolutionary_parameter_values:
            evolutionary_parameter_values.append(evolutionary_parameter_value.get())
        x = []
        y = []
        for i in range(problem_size, problem_size_end+1, step):
            print("Problem size: " + str(i))
            results = np.empty(iterations)
            for j in range(iterations):
                _, results[j], _, _, _ = self.evolutionary_algorithm.solve(evolutionary_parameter_values,
                                                                           i,
                                                                           self.fitness_function,
                                                                           fitness_parameter_values)
            x.append(i)
            y.append(round(results.mean(), 0))

        build_graph(self, [self.evolutionary_algorithm.name], [x], [y], start_row, 2, "Test", "Problem size", "Mean of the runs")


class RKNM(ActionInterface):

    def __init__(self, class_name, parent, controller, action,
                 problem_size, problem_size_end, step, iterations,
                 fitness_function, fitness_parameter_values,
                 evolutionary_algorithm, evolutionary_parameter_values, labels, xs, ys):

        super().__init__(class_name, parent, controller, action,
                         problem_size, problem_size_end, step, iterations,
                         fitness_function, fitness_parameter_values,
                         evolutionary_algorithm, evolutionary_parameter_values, labels, xs, ys)

        row = self.choice_of_problem_range(2)
        row = self.choice_of_number_of_iterations(row)
        fitness_row = self.choice_of_fitness_function(row)
        row = self.choice_of_fitness_parameters(fitness_row)
        evolutionary_row = self.choice_of_evolutionary_algorithm(row)
        row = self.choice_of_evolutionary_parameters(evolutionary_row)

        # Create the graph of the fitness function
        display_button = ttk.Button(self, text="New run", command=lambda: self.new_run(row+1))
        display_button.grid(row=row, column=2, padx=5, pady=5)

        if len(self.labels) > 0:
            # Add a new run from the previous graph
            display_button = ttk.Button(self, text="Add run",
                                        command=lambda: self.solve_k_n_m_times(row+1))
            display_button.grid(row=row, column=3, padx=5, pady=5)

    def solve_k_n_m_times(self, start_row):
        problem_size = self.problem_size.get()
        problem_size_end = self.problem_size_end.get()
        step = self.step.get()

        iterations = self.iterations.get()
        fitness_parameter_values = []
        for fitness_parameter_value in self.fitness_parameter_values:
            fitness_parameter_values.append(fitness_parameter_value.get())
        evolutionary_parameter_values = []
        for evolutionary_parameter_value in self.evolutionary_parameter_values:
            evolutionary_parameter_values.append(evolutionary_parameter_value.get())
        x = []
        y = []
        for i in range(problem_size, problem_size_end + 1, step):
            print("Problem size: " + str(i))
            results = np.empty(iterations)
            for j in range(iterations):
                _, results[j], _, _, _ = self.evolutionary_algorithm.solve(evolutionary_parameter_values,
                                                                           i,
                                                                           self.fitness_function,
                                                                           fitness_parameter_values)
            x.append(i)
            y.append(round(results.mean(), 0))

        self.labels.append(self.evolutionary_algorithm.name)
        self.xs.append(x)
        self.ys.append(y)

        build_graph(self, self.labels, self.xs, self.ys, start_row, 2,
                    "Comparison of different algorithms on " + self.fitness_function_name.get(),
                    "Problem size", "Mean of the runs")

        # Add a button for adding a new run from the previous graph
        display_button = ttk.Button(self, text="Add run",
                                    command=lambda: self.solve_k_n_m_times(start_row))
        display_button.grid(row=start_row-1, column=3, padx=5, pady=5)

    def new_run(self, start_row):
        self.labels = []
        self.xs = []
        self.ys = []
        self.solve_k_n_m_times(start_row)


