import random


class BitString:

    # Generates a random bit string of length "size
    def __init__(self, size):
        self.string = ""
        for i in range(size):
            self.string += str(random.randint(0, 1))

    # Switch every bit with a probability of p
    def create_offspring(self, p):
        # Creation of the new bit string by flipping bits from the previous bit string
        new_string = ""
        for bit in self.string:
            if random.random() < p:
                new_string += str(1 - int(bit))
            else:
                new_string += bit
        new_bit_string = BitString(0)
        new_bit_string.string = new_string
        return new_bit_string

    def only_zeros(self):
        self.string = "0" * len(self.string)

    def only_ones(self):
        self.string = "1" * len(self.string)

    def add_one_one(self):
        new_string = ""
        i = 0
        while i < len(self.string) and self.string[i] == "1":
            new_string += "1"
            i += 1
        if i < len(self.string):
            new_string += "1"
            i += 1
        else:
            raise Exception("Can't add any one to the full only ones string")
        for j in range(i, len(self.string)):
            new_string += self.string[j]
        self.string = new_string
