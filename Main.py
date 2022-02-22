from Interface import *


class MainInterface(tk.Tk):

    def __init__(self, *args, **kwargs):

        # init function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Framework")
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry("%dx%d" % (width, height))

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initialising frames to an empty set
        self.frames = {}
        frame = StartPage(StartPage, container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        self.frames[StartPage] = frame

        # Create a frame for each action
        for action in actions:
            class_name = globals()[action.name]
            # Set default values for problem size and number of iterations
            problem_size = IntVar()
            problem_size.set(60)
            problem_size_end = IntVar()
            problem_size_end.set(120)
            step = IntVar()
            step.set(10)
            iterations = IntVar()
            iterations.set(100)
            # Create the action frame
            frame = class_name(class_name, container, self, action,
                               problem_size, problem_size_end, step, iterations,
                               evolutionary_algorithms[0],
                               default_parameters(evolutionary_algorithms[0], problem_size.get()),
                               fitness_functions[0], default_parameters(fitness_functions[0], problem_size.get()))
            self.frames[class_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    # Show the selected frame
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


def main():
    main_interface = MainInterface()
    main_interface.mainloop()


main()
