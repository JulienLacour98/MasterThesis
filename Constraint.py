class Constraint:

    def __init__(self, name, description, condition):
        self.name = name
        self.description = description
        self.condition = condition

    def check_condition(self, element):
        return self.condition(element)


def is_integer(element):
    return str(element).isnumeric()


def multiple_of_2(element):
    return int(element) % 2 == 0


def multiple_of_4(element):
    return int(element) % 4 == 0


INT = Constraint("INT", "This has to be an integer", is_integer)
M2 = Constraint("M2", "This integer has to be a multiple of 2", multiple_of_2)
M4 = Constraint("M4", "This integer has to be a multiple of 4", multiple_of_4)



