from Actions import *
from utilities import *


# Main function
def main():
    action, action_parameters = choose_element("Action", actions, 0)
    action.algorithm()


main()
