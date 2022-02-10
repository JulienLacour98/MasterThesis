def choose_element(name, array, size):
    print("")
    print(name + ":")
    for i in range(len(array)):
        array[i].update_parameters(size)
        print("    - " + str(i + 1) + ": " + array[i].name)
    chosen = False
    while not chosen:
        element_index = input("Choose the " + name.lower() + ": ")
        # Checking that the number is an integer
        if element_index.isnumeric():
            element_index = int(element_index) - 1
            # Checking that the integer is the index of an element
            if element_index in range(len(array)):
                chosen = True
                element = array[element_index]
                # Selection of the value of the parameters
                element_parameters = []
                for parameter in element.parameters:
                    chosen_parameter = False
                    while not chosen_parameter:
                        input_parameter = input("Enter parameter " + parameter.name + " of the " + name.lower() + ": ")
                        # Checking that the value of the parameter is valid
                        if parameter.is_value_valid(input_parameter):
                            element_parameters.append(input_parameter)
                            chosen_parameter = True
            else:
                print("Your integer has to be between 1 and " + str(len(array)))
        else:
            print("It has to be an integer")
    return element, element_parameters


def choose_integer(name, mini, maxi):
    print("")
    chosen = False
    while not chosen:
        integer = input("Choose the " + name.lower() + ": ")
        # Checking that the number is an integer
        if integer.isnumeric():
            integer = int(integer)
            # Checking that the integer is in the range [mini, maxi]
            if mini <= integer <= maxi:
                chosen = True
            else:
                print("Your integer has to between " + str(mini) + " and " + str(maxi))
        else:
            print("It has to be an integer")
    return integer

