import random


class BitString:

    def __init__(self, size):
        self.string = ""
        for i in range(size):
            self.string += str(random.randint(0, 1))

