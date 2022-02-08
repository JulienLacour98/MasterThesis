import random


class BitString:

    # Generates a random bit string of length "size
    def __init__(self, size):
        self.string = ""
        for i in range(size):
            self.string += str(random.randint(0, 1))
