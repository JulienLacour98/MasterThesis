class Action:

    def __init__(self, name, folder_name, description):
        self.name = name
        self.folder_name = folder_name
        self.description = description
        actions.append(self)


actions = []

# Creation of Display Fitness
DisplayFitness = Action("DF", "1_display_fitness", "1 - Display the graph of a fitness function")

# Creation of Run Once
RunOnce = Action("R1", "2_run_once", "2 - Display a run of an evolutionary algorithm on a fitness function")

# Creation of Run n Times
RunNTimes = Action("RN", "3_statistical_fixed_length",
                   "3 - Statistical analysis of an evolutionary algorithm on a fitness function and fixed problem size")

# Creation of Run or a range of problem sizes
RunFromNtoM = Action("RNM", "4_statistical_range_lengths",
                     "4 - Statistical analysis of one evolutionary algorithm on a fitness function "
                     "for a range of problem sizes")

# Creation of Run k fitness function for a range of problem sizes
RunKFromNtoM = Action("RKNM", "5_comparison_algorithms",
                      "5 - Comparison of several evolutionary algorithms on a fitness function"
                      "for a range of problem sizes")

# Creation of the SAT Solving page
SAT_Solving = Action("ISAT", "6_SAT",
                     "6 - Solve a MAX-SAT problem")

# Creation of the SAT Solving page
SATS_Solving = Action("ISATS", "7_SATS",
                      "7 - Statistical analysis on MAX-SAT problems")
