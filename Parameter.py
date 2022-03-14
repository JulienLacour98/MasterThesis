import math
import numpy as np


class Parameter:

    def __init__(self, name, parameter_type, default_value, min_value, max_value, constraint):
        self.name = name
        self.parameter_type = parameter_type
        self.default_value = default_value
        self.min_value = min_value
        self.max_value = max_value
        self.constraint = constraint

    # Checking that the value is of the right type and that it is in between the min and max values
    def is_value_valid(self, value, size_start, size_end):
        if self.parameter_type == "integer":
            if not str(value).isnumeric():
                return "It has to be an integer"
            else:
                min_value = max(update_parameter(self.min_value, size_start),
                                update_parameter(self.min_value, size_end))
                max_value = min(update_parameter(self.max_value, size_start),
                                update_parameter(self.max_value, size_end))
                if min_value <= value <= max_value:
                    if self.constraint.check_condition(value):
                        return "correct"
                    else:
                        return self.constraint.description
                else:
                    return "The integer has to be between " + str(min_value) + " and " + str(max_value)
        else:
            raise Exception("Unknown parameter's type")


# Return the correct value if it depends on the problem size
def update_parameter(value, size):
    if value == "size":
        return size
    elif value == "size^3":
        return np.power(size, 3)
    elif value == "log(size)":
        return int(math.ceil(math.log(size)))
    elif value == "size/2":
        return int(size/2)
    elif value == "size/4":
        return int(size/4)
    elif value == "sqrt*log":
        return math.ceil(math.sqrt(size) * math.log(size))
    else:
        return value
            