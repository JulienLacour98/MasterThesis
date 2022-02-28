import functools


class Constraint:

    def __init__(self, name, description, condition):
        self.name = name
        self.description = description
        self.condition = condition

    def check_condition(self, element):
        return self.condition(element)


# Return True if the element is an integer
def is_integer(element):
    return str(element).isnumeric()


# Return True if the element is a multiple of k
def multiple_of_k(k, element):
    return int(element) % k == 0


INT = Constraint("INT", "This has to be an integer", is_integer)
M2 = Constraint("M2", "This integer has to be a multiple of 2", functools.partial(multiple_of_k, 2))
M4 = Constraint("M4", "This integer has to be a multiple of 4", functools.partial(multiple_of_k, 4))



