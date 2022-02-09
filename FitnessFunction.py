from Parameter import *


class FitnessFunction:

    def __init__(self, name, description, parameters, function, function_maximum):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.function = function
        self.function_maximum = function_maximum

    # Update the min and max of the parameters if they depend on the size of the problem
    def update_parameters(self, size):
        for parameter in self.parameters:
            parameter.update_parameter(size)

    # Return the image of the fitness function for the bit string
    def result(self, parameters, size, bit_string):
        return self.function(parameters, size, bit_string.string)

    # Return the maximum of the fitness function for a selected size
    def maximum(self, parameters, size):
        return self.function_maximum(parameters, size)


# Definition of the OneMax function
def one_max(parameters, size, bit_string):
    return bit_string.count('1')


# Function returning the maximum of the OneMax function
def one_max_maximum(parameters, size):
    if size < 0:
        raise Exception("Negative size")
    return size


# Definition of the Jump function
def jump_m(parameters, size, bit_string):
    m = int(parameters[0])
    norm = bit_string.count('1')
    if norm <= size - m or norm == size:
        return m + norm
    else:
        return size - norm


# Function returning the maximum of the Jump function
def jump_m_maximum(parameters, size):
    return int(parameters[0]) + size


# Definition of the JumpOffset function
def jump_offset_m(parameters, size, bit_string):
    m = int(parameters[0])
    norm = bit_string.count('1')
    if norm <= 3 * size/4 or norm >= 3 * size/4 + m:
        return m + norm
    else:
        return 3 * size/4 + m - norm


# Function returning the maximum of the JumpOffset function
def jump_offset_m_maximum(parameters, size):
    return int(parameters[0]) + size


# Definition of the JumpOffsetSpike function
def jump_offset_spike_m(parameters, size, bit_string):
    m = int(parameters[0])
    norm = bit_string.count('1')
    if norm <= 3 * size/4 or norm >= 3 * size/4 + m:
        return m + norm
    elif norm == 3*size/4 + m/2:
        return size + m + 1
    else:
        return 3*size/4 + m - norm


# Function returning the maximum of the JumpOffsetSpike function
def jump_offset_spike_m_maximum(parameters, size):
    return size + int(parameters[0]) + 1


# List containing every fitness functions
fitness_functions = []

# Creation of OneMax
OneMax = FitnessFunction("OneMax", "Returns the number of ones in the bit string.", [], one_max, one_max_maximum)
fitness_functions.append(OneMax)

# Creation of Jump
gap_m = Parameter("m", "integer", 0, "size")
JumpM = FitnessFunction("Jump_m",
                        "Function with a local minimum followed by a gap of size m and then the global maximum.",
                        [gap_m],
                        jump_m,
                        jump_m_maximum)
fitness_functions.append(JumpM)

# Creation of JumpOffset
gap_m = Parameter("m", "integer", 0, "size")
JumpOffsetM = FitnessFunction("JumpOffset_m",
                              "Function with a local minimum followed by a gap of size m and then a ramp going to "
                              "the global maximum.",
                              [gap_m],
                              jump_offset_m,
                              jump_offset_m_maximum)
fitness_functions.append(JumpOffsetM)

# Creation of JumpOffsetSpike
gap_m = Parameter("m", "integer", 0, "size")
JumpOffsetSpikeM = FitnessFunction("JumpOffsetSpike_m",
                                   "Function with a local minimum followed by a gap of size m with the global optimum "
                                   "in the middle then a ramp going to.",
                                   [gap_m],
                                   jump_offset_spike_m,
                                   jump_offset_spike_m_maximum)
fitness_functions.append(JumpOffsetSpikeM)
