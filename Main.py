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
            problem_size.set(80)
            problem_size_end = IntVar()
            problem_size_end.set(160)
            step = IntVar()
            step.set(20)
            iterations = IntVar()
            iterations.set(1000)
            fitness_function_name = StringVar()
            fitness_function_name.set(fitness_function_names[0])
            evolutionary_algorithm_name = StringVar()
            evolutionary_algorithm_name.set(evolutionary_algorithm_names[0])
            # Create the action frame
            frame = class_name(class_name, container, self, action,
                               problem_size, problem_size_end, step, iterations,
                               fitness_function_name,
                               default_parameters(find_fitness(fitness_function_name.get()), problem_size.get()),
                               evolutionary_algorithm_name,
                               default_parameters(find_evolutionary(evolutionary_algorithm_name.get()),
                                                  problem_size.get()),
                               [], [], [])
            self.frames[class_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    # Show the selected frame
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


def main():

    if __name__ == "__main__":
        main_interface = MainInterface()
        main_interface.mainloop()


main()
