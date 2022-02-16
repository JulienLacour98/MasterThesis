import tkinter as tk
from tkinter import *
from tkinter import ttk

from Action import *
from FitnessFunction import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


class Interface(tk.Frame):

    def __init__(self, class_name):
        self.class_name = class_name
        interfaces.append(self)


class ActionInterface(Interface):

    def __init__(self, class_name, action):
        super().__init__(class_name)
        self.action = action
        action_interfaces.append(self)


class StartPage(Interface):
    def __init__(self, class_name, parent, controller):
        super().__init__(class_name)
        self.parent = parent
        self.controller = controller

        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Choose an action:")
        label.grid(row=0, column=0, padx=10, pady=10)

        for i in range(len(action_interfaces)):
            ttk.Button(self, text=action_interfaces[i].action.description,
                       command=lambda i=i: controller.show_frame(action_interfaces[i].class_name))\
                .grid(row=i+1, column=1, padx=10, pady=10)


class DF(ActionInterface):

    def __init__(self, class_name, action, parent, controller, fitness_function=fitness_functions[0]):
        super().__init__(class_name, action)
        self.parent = parent
        self.controller = controller

        tk.Frame.__init__(self, parent)
        tk.Label(self, text=action.description).grid(row=0, column=0, padx=10, pady=10)

        # Button back to main page
        button = ttk.Button(self, text="Back to Start Page",
                            command=lambda: controller.show_frame(StartPage))
        button.grid(row=0, column=3, padx=10, pady=10)

        tk.Label(self, text="Choose a fitness function: ").grid(row=1, column=0, padx=10, pady=10)
        self.chosen_fitness_name = StringVar()
        self.chosen_fitness_name.set(fitness_function.name)
        self.chosen_fitness = find_fitness(self.chosen_fitness_name.get())
        choose_fitness = OptionMenu(self,
                                    self.chosen_fitness_name,
                                    *fitness_functions_names,
                                    command=self.change_fitness)
        choose_fitness.grid(row=1, column=1, padx=10, pady=10)
        problem_size = IntVar()
        problem_size.set(100)
        parameters = fitness_function.parameters
        self.parameters_values = []
        tk.Label(self, text="Choose parameters:").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(self, text="Problem Size:").grid(row=3, column=1, padx=10, pady=10)
        tk.Entry(self, justify=CENTER, textvariable=problem_size).grid(row=3, column=2, padx=10, pady=10)
        for i in range(len(parameters)):
            parameter_value = tk.IntVar()
            tk.Label(self, text=parameters[i].name).grid(row=i+4, column=1, padx=10, pady=10)
            tk.Entry(self, justify=CENTER, textvariable=parameter_value).grid(row=i+4, column=2, padx=10, pady=10)
            self.parameters_values.append(parameter_value)

        display_button = ttk.Button(self, text="Display graph", command=lambda: self.display_graph(problem_size.get()))
        display_button.grid(row=len(parameters)+4, column=2, padx=10, pady=10)

    def change_fitness(self, *args):
        self.chosen_fitness = find_fitness(self.chosen_fitness_name.get())
        new_frame = DF(self.class_name, self.action, self.parent, self.controller, self.chosen_fitness)
        new_frame.grid(row=0, column=0, sticky="nsew")
        new_frame.tkraise()

    def display_graph(self, problem_size):
        parameters = []
        for param in self.parameters_values:
            parameters.append(param.get())

        bit_string = BitString(problem_size)
        bit_string.only_zeros()
        x = np.empty(problem_size + 1)
        y = np.empty(problem_size + 1)
        x[0] = 0
        y[0] = self.chosen_fitness.result(parameters, problem_size, bit_string)
        for i in range(problem_size):
            bit_string.add_one_one()
            x[i + 1] = i + 1
            y[i + 1] = self.chosen_fitness.result(parameters, problem_size, bit_string)

        fig = Figure(figsize=(5, 4), dpi=100)
        fig.add_subplot(111).plot(x, y, '.')

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=len(self.parameters_values)+5, column=2, padx=10, pady=10)

        toolbar_frame = Frame(self)
        toolbar_frame.grid(row=len(self.parameters_values)+6, column=2)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
        canvas.get_tk_widget().grid(row=len(self.parameters_values)+5, column=2, padx=10, pady=10)


class R1(ActionInterface):

    def __init__(self, class_name, action, parent, controller):
        super().__init__(class_name, action)
        self.parent = parent
        self.controller = controller

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text=action.description)
        label.grid(row=0, column=0, padx=10, pady=10)

        # Button back to main page
        button = ttk.Button(self, text="Back to Start Page",
                            command=lambda: controller.show_frame(StartPage))
        button.grid(row=1, column=1, padx=10, pady=10)


class RN(ActionInterface):

    def __init__(self, class_name, action, parent, controller):
        super().__init__(class_name, action)
        self.parent = parent
        self.controller = controller

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text=action.description)
        label.grid(row=0, column=0, padx=10, pady=10)

        # Button back to main page
        button = ttk.Button(self, text="Back to Start Page",
                            command=lambda: controller.show_frame(StartPage))
        button.grid(row=1, column=1, padx=10, pady=10)


def find_fitness(fitness_name):
    for fitness_function in fitness_functions:
        if fitness_function.name == fitness_name:
            return fitness_function
    raise Exception("Fitness function not found")


interfaces = []
action_interfaces = []

StartPageInterface = Interface(StartPage)
DFInterface = ActionInterface(DF, DisplayFitness)
# R1Interface = ActionInterface(R1, RunOnce)
# RNInterface = ActionInterface(RN, RunNTimes)
