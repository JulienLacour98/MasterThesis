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

        # initialising frames to an empty array
        self.frames = {}

        for i in range(len(interfaces)):
            interface = interfaces[i]
            if isinstance(interface, ActionInterface):
                frame = interface.class_name(interface.class_name, interface.action, container, self)
            else:
                frame = interface.class_name(interface.class_name, container, self)
            self.frames[interface.class_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


def main():
    main_interface = MainInterface()
    main_interface.mainloop()


main()
