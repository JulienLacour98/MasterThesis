import random


class BitString:

    # Generates a random bit string of length "size
    def __init__(self, size):
        self.string = ""
        for i in range(size):
            self.string += str(random.randint(0, 1))

    # Flip every bit with a probability of p
    def create_offspring_p(self, p):
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

    # Flip s bits uniformly // TODO- Check correctness (used from "Algorithmic Techniques for Modern Data Models")
    def create_offspring_s(self, s):
        n = len(self.string)
        # Reservoir sampling algorithm
        # It is an algorithm for choosing uniformly s elements out of n
        if s <= n:
            flipping_bits = list(range(s))
            for i in range(s, n):
                if random.random() < s/(i+1):
                    idx = random.randrange(0, s)
                    flipping_bits[idx] = i
            new_bit_string = BitString(0)
            for i in range(n):
                if i in flipping_bits:
                    new_bit_string.string += str(1 - int(self.string[i]))
                else:
                    new_bit_string.string += self.string[i]
            return new_bit_string
        else:
            raise Exception("It is not possible to flip more than the number of bits in the string")

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
            raise Exception("Can't add any one to the only ones string")
        for j in range(i, len(self.string)):
            new_string += self.string[j]
        self.string = new_string
