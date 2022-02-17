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
                        print(constraint.description)
                        valid = False
                return valid
            else:
                print("The value has to be an integer between " + str(self.min_value) + " and " + str(self.max_value))
                return False
        else:
            raise Exception("Unknown parameter's type")

    # Update the min and max values of the parameter if it depends on the size of the problem
    def update_parameter(self, size):
        if self.min_value == "size":
            self.min_value = size
        if self.max_value == "size":
            self.max_value = size
            