import os


class SAT:

    def __init__(self, path):
        if os.path.exists(path):
            # TODO - Create a function to extract the name of the file from the path
            self.name = os.path.basename(path)

            with open(path) as f:
                line = f.readline().split()

                while line[0] == 'c':
                    line = f.readline().split()

                if line[0] == 'p':
                    if line[1] == 'cnf':
                        self.number_of_variables = int(line[2])
                        self.number_of_clauses = int(line[3])
                    else:
                        raise Exception("Parameters are not defined correctly")

                self.clauses = []
                new_clause = []
                while len(self.clauses) < self.number_of_clauses:
                    line = f.readline().split()
                    for variable in line:
                        if variable == '0':
                            self.clauses.append(new_clause)
                            new_clause = []
                        elif abs(int(variable)) in range(1, self.number_of_variables + 1):
                            new_clause.append(int(variable))
                        else:
                            raise Exception("Variable outside of bound")
                if len(self.clauses) != self.number_of_clauses:
                    raise Exception("More clauses than announced")
        else:
            self.name = "No file selected"
            self.number_of_variables = 0
            self.number_of_clauses = 0
            self.clauses = []

    # Return the image of the fitness function for the bit string
    def result(self, _,  bit_string):
        if len(bit_string.string) == self.number_of_variables:
            satisfied_clauses = 0
            for clause in self.clauses:
                i = 0
                satisfied = False
                while i < len(clause) and not satisfied:
                    if clause[i] > 0:
                        variable = clause[i] - 1
                        value = '1'
                    else:
                        variable = - clause[i] - 1
                        value = '0'
                    satisfied = (value == bit_string.string[variable])
                    i += 1
                if satisfied:
                    satisfied_clauses += 1
            return satisfied_clauses
        else:
            raise Exception("Bit string of the wrong length")

    def maximum(self, _, size):
        # TODO - Change when all clauses are not solvable
        return self.number_of_clauses
