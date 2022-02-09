import random


class BitString:

    # Generates a random bit string of length "size
    def __init__(self, size):
        self.string = ""
        for i in range(size):
            self.string += str(random.randint(0, 1))

    def create_offspring(self, p):
        # Creation of the new bit string by flipping bits from the previous bit string
        new_string = ""
        for bit in self.string:
            if random.random() < p:
                new_bit = str(1 - int(bit))
                new_string += new_bit
            else:
                new_string += bit
        new_bit_string = BitString(0)
        new_bit_string.string = new_string
        return new_bit_string
