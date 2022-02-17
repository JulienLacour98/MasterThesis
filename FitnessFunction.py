import math
from Parameter import *


class FitnessFunction:

    def __init__(self, name, parameters, function, function_maximum):
        self.name = name
        self.parameters = parameters
        self.function = function
        self.function_maximum = function_maximum
        fitness_functions.append(self)
        fitness_function_names.append(self.name)

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
    m = parameters[0]
    norm = bit_string.count('1')
    if norm <= size - m or norm == size:
        return m + norm
    else:
        return size - norm


# Function returning the maximum of the Jump function
def jump_m_maximum(parameters, size):
    return parameters[0] + size


# Definition of the JumpOffset function
def jump_offset_m(parameters, size, bit_string):
    m = parameters[0]
    norm = bit_string.count('1')
    if norm <= 3 * size/4 or norm >= 3 * size/4 + m:
        return m + norm
    else:
        return 3 * size/4 + m - norm


# Function returning the maximum of the JumpOffset function
def jump_offset_m_maximum(parameters, size):
    return parameters[0] + size


# Definition of the JumpOffsetSpike function
def jump_offset_spike_m(parameters, size, bit_string):
    m = parameters[0]
    norm = bit_string.count('1')
    if norm <= 3 * size/4 or norm >= 3 * size/4 + m:
        return m + norm
    elif norm == 3*size/4 + m/2:
        return size + m + 1
    else:
        return 3*size/4 + m - norm


# Function returning the maximum of the JumpOffsetSpike function
def jump_offset_spike_m_maximum(parameters, size):
    return size + parameters[0] + 1


# Definition of the Cliff function
def cliff_d(parameters, size, bit_string):
    d = parameters[0]
    norm = bit_string.count('1')
    if norm <= size - d:
        return norm
    else:
        return norm - d + 1/2


# Function returning the maximum of the Cliff function
def cliff_d_maximum(parameters, size):
    d = parameters[0]
    return size - d + 1/2


# Definition of the Hurdle function
def hurdle_w(parameters, size, bit_string):
    w = parameters[0]
    z = bit_string.count('0')
    r = z % w
    return - math.ceil(z/w) - r/w


# Function returning the maximum of the Hurdle function
def hurdle_w_maximum(parameters, size):
    return 0

# TODO - Update default values


# List containing every fitness functions
fitness_functions = []
fitness_function_names = []

# Creation of OneMax
OneMax = FitnessFunction("OneMax", [], one_max, one_max_maximum)

# Creation of Jump
gap_m = Parameter("m", "integer", 3, 1, "size", [])
JumpM = FitnessFunction("Jump_m", [gap_m], jump_m, jump_m_maximum)

# Creation of JumpOffset
gap_m = Parameter("m", "integer", 3, 1, "size", [])
JumpOffsetM = FitnessFunction("JumpOffset_m", [gap_m], jump_offset_m, jump_offset_m_maximum)

# Creation of JumpOffsetSpike
gap_m = Parameter("m", "integer", 4, 2, "size", [M2])
JumpOffsetSpikeM = FitnessFunction("JumpOffsetSpike_m", [gap_m], jump_offset_spike_m, jump_offset_spike_m_maximum)

# Creation of Cliff
gap_d = Parameter("d", "integer", 3, 1, "size", [])
CliffD = FitnessFunction("Cliff_d", [gap_d], cliff_d, cliff_d_maximum)

# Creation of Hurdle
param_w = Parameter("w", "integer", 10, 1, float('inf'), [])
HurdleW = FitnessFunction("Hurdle_w", [param_w], hurdle_w, hurdle_w_maximum)
