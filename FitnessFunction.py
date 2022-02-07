class FitnessFunction:

    def __init__(self, name, description, function, function_maximum):
        self.name = name
        self.description = description
        self.function = function
        self.function_maximum = function_maximum

    def result(self, bit_string):
        if not all(bit in '01' for bit in bit_string):
            raise Exception("Argument is not a bit string")
        else:
            return self.function(bit_string)

    def maximum(self, size):
        return self.function_maximum(size)


fitness_functions = []


def one_max(bit_string):
    return bit_string.count('1')


def one_max_maximum(size):
    if size < 0:
        raise Exception("Negative size")
    return size


OneMax = FitnessFunction("OneMax", "Returns the number of ones in the bit string", one_max, one_max_maximum)
fitness_functions.append(OneMax)
