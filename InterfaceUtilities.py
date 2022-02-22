import tkinter as tk
from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

from EvolutionaryAlgorithm import *
from FitnessFunction import *


# Create frame with return button if not the main page
def frame_creation(root, title, start_page=False):
    # Creation of the frame
    tk.Frame.__init__(root, root.parent)

    # Title of the page
    label = tk.Label(root, text=title, font=("Arial", 20))
    label.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

    # Add return button
    if start_page:
        # Button back to main page
        button = ttk.Button(root, text="Return to main page",
                            command=lambda: root.controller.show_frame(start_page))
        button.grid(row=0, column=4, padx=5, pady=5)


# Return the evolutionary algorithm with the input name
def find_evolutionary(evolutionary_name):
    for evolutionary_algorithm in evolutionary_algorithms:
        if evolutionary_algorithm.name == evolutionary_name:
            return evolutionary_algorithm
    raise Exception("Evolutionary algorithm not found")


# Return the fitness function with the input name
def find_fitness(fitness_name):
    for fitness_function in fitness_functions:
        if fitness_function.name == fitness_name:
            return fitness_function
    raise Exception("Fitness function not found")


# Build a graph with the x and y values
def build_graph(root, x, y, row, column, title, x_label, y_label):
    fig = Figure(figsize=(6, 4), dpi=100)
    a = fig.add_subplot(111)

    a.set_title(title)
    a.set_xlabel(x_label)
    a.set_ylabel(y_label)

    a.plot(x, y, '.')

    canvas = FigureCanvasTkAgg(fig, root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=row, column=column, padx=5, pady=5)

    toolbar_frame = Frame(root)
    toolbar_frame.grid(row=row+1, column=column)
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
    toolbar.update()
    canvas.get_tk_widget().grid(row=row, column=column, padx=5, pady=5)


# Return an array with the default value of the parameters of the element
def default_parameters(element, size):
    parameter_values = []
    for parameter in element.parameters:
        parameter_value = IntVar()
        parameter_value.set(update_parameter(parameter.default_value, size))
        parameter_values.append(parameter_value)
    return parameter_values
