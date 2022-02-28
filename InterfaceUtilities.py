import os
import pandas as pd
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
        button.grid(row=0, column=3, padx=5, pady=5)


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
def build_plot(root, labels, xs, ys, row, column, title, x_label, y_label):
    fig = Figure(figsize=(6, 4), dpi=100)
    a = fig.add_subplot(111)

    # Setting the title and axis labels
    a.set_title(title)
    a.set_xlabel(x_label)
    a.set_ylabel(y_label)

    # Plotting all the plots, adding the label names
    for i in range(len(labels)):
        a.plot(xs[i], ys[i], '.', label=labels[i][1])

    # If there is more than one plot, the legend is displayed on the left corner
    if len(labels) > 1:
        a.legend(loc='upper left', frameon=False)

    # Creation of the canvas
    canvas = FigureCanvasTkAgg(fig, root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=row, column=column, columnspan=2, padx=5, pady=5)

    # Creation of the toolbar, displayed under the graph
    toolbar_frame = Frame(root)
    toolbar_frame.grid(row=row+1, column=column)
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
    toolbar.update()
    canvas.get_tk_widget().grid(row=row, column=column, columnspan=2, padx=5, pady=5)

    # Button to extract data
    button = ttk.Button(root, text="Download data",
                        command=lambda: extract_data(labels, xs, ys))
    button.grid(row=row+1, column=column+1, padx=5, pady=5)


def extract_data(labels, xs, ys):

    j = 0
    while os.path.exists("../export/export%s.xlsx" % j):
        j += 1

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter("../export/export" + str(j) + ".xlsx", engine="xlsxwriter")

    for i in range(len(labels)):
        df = pd.DataFrame()
        df[labels[i][0]] = xs[i]
        df[labels[i][1]] = ys[i]
        df.to_excel(writer, sheet_name=(str(i+1) + " " + labels[i][1]))
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()


# Build a graph with the x and y values
def build_box_plot(root, x, y, row, column, title, x_label, y_label):
    fig = Figure(figsize=(6, 4), dpi=100)
    a = fig.add_subplot(111)

    # Setting the title and axis labels
    a.set_title(title)
    a.set_xlabel(x_label)
    a.set_ylabel(y_label)

    # Plotting the box plot
    a.boxplot(y, labels=x)

    # Creation of the canvas
    canvas = FigureCanvasTkAgg(fig, root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=row, column=column, columnspan=2, padx=5, pady=5)

    # Creation of the toolbar, displayed under the graph
    toolbar_frame = Frame(root)
    toolbar_frame.grid(row=row+1, column=column)
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
    toolbar.update()
    canvas.get_tk_widget().grid(row=row, column=column, columnspan=2,  padx=5, pady=5)


# Return an array with the default value of the parameters of the element
def default_parameters(element, size):
    parameter_values = []
    for parameter in element.parameters:
        parameter_value = IntVar()
        # Get default value, which can be a function of the problem size
        parameter_value.set(update_parameter(parameter.default_value, size))
        parameter_values.append(parameter_value)
    return parameter_values
