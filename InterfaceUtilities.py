import tkinter as tk
from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

from EvolutionaryAlgorithm import *
from FitnessFunction import *


def frame_creation(root, title, start_page=False):
    # Creation of the frame
    tk.Frame.__init__(root, root.parent)

    # Title of the page
    label = tk.Label(root, text=title, font=("Arial", 20))
    label.grid(row=0, column=0, padx=10, pady=10)

    # Add return button
    if start_page:
        # Button back to main page
        button = ttk.Button(root, text="Return to main page",
                            command=lambda: root.controller.show_frame(start_page))
        button.grid(row=0, column=10, padx=10, pady=10)


def find_evolutionary(evolutionary_name):
    for evolutionary_algorithm in evolutionary_algorithms:
        if evolutionary_algorithm.name == evolutionary_name:
            return evolutionary_algorithm
    raise Exception("Evolutionary algorithm not found")


def find_fitness(fitness_name):
    for fitness_function in fitness_functions:
        if fitness_function.name == fitness_name:
            return fitness_function
    raise Exception("Fitness function not found")


def build_graph(root, x, y, row, column):
    fig = Figure(figsize=(5, 4), dpi=100)
    fig.add_subplot(111).plot(x, y, '.')

    canvas = FigureCanvasTkAgg(fig, root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=row, column=column, padx=10, pady=10)

    toolbar_frame = Frame(root)
    toolbar_frame.grid(row=row+1, column=column)
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
    toolbar.update()
    canvas.get_tk_widget().grid(row=row, column=column, padx=10, pady=10)


