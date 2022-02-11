from Actions import *
from utilities import *


# Main function
def main():
    stop = False
    while not stop:
        action, action_parameters = choose_element("Action", actions, 0)
        action.algorithm()
        string = input("Enter 0 to exit: ")
        if string == "0":
            stop = True


main()
