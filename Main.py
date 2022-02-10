from Actions import *


# Main function
def main():
    print("Action:")
    for i in range(len(actions)):
        print("    - " + str(i + 1) + ": " + actions[i].name)
    chosen_action = False
    while not chosen_action:
        action_index = input("Choose an action: ")
        # Checking that the number is an integer
        if action_index.isnumeric():
            action_index = int(action_index) - 1
            # Checking that the integer is the index of one of the actions
            if action_index in range(len(actions)):
                chosen_action = True
                action = actions[action_index]
                # Selection of the value of the parameters
                action_parameters = []
                for parameter in action.parameters:
                    chosen_parameter = False
                    while not chosen_parameter:
                        input_parameter = input("Enter parameter " + parameter.name + " of the action: ")
                        # Checking that the value of the parameter is valid
                        if parameter.is_value_valid(input_parameter):
                            action_parameters.append(input_parameter)
                            chosen_parameter = True
            else:
                print("Your integer has to be between 1 and " + str(len(actions)))
        else:
            print("It has to be an integer")
    action.algorithm()


main()
