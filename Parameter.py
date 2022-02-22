import math
import numpy as np


class Parameter:

    def __init__(self, name, parameter_type, default_value, min_value, max_value, constraints):
        self.name = name
        self.parameter_type = parameter_type
        self.default_value = default_value
        self.min_value = min_value
        self.max_value = max_value
        self.constraints = constraints

    # Checking that the value is of the right type and that it is in between the min and max values
    def is_value_valid(self, value):
        if self.parameter_type == "integer":
            if value.isnumeric() and self.min_value <= int(value) <= self.max_value:
                valid = True
                for constraint in self.constraints:
                    if not constraint.check_condition(value):
                        valid = False
                return valid
            else:
                return False
        else:
            raise Exception("Unknown parameter's type")


# Update the min and max values of the parameter if it depends on the size of the problem
def update_parameter(value, size):
    if value == "size":
        return size
    elif value == "size^3":
        return np.power(size, 3)
    elif value == "log(size)":
        return math.ceil(math.log(size))
    elif value == "size/2":
        return size/2
    elif value == "size/4-1":
        return size/4 - 1
    else:
        return value
            