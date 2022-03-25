import math
import os.path
from Interface import *


# Evaluate all the algorithms on OneMax
def script_1(start_length, end_length, length_step, runs, nb_cores, excel):
    # Create array with all the length analysed
    lengths = []
    for iteration in range(start_length, end_length + 1, length_step):
        lengths.append(iteration)

    results = []
    means = []
    # For each algorithm and each length, run the algorithm "runs" time
    for i in range(len(evolutionary_algorithms)):
        results.append([])
        means.append([])
        header = ""
        for j in range(len(lengths)):
            header += evolutionary_algorithms[i].name + " " + str(lengths[j]) + ";"
            print("Lengths: " + str(lengths[j]))
            print("Parameters: " + str(default_parameters(evolutionary_algorithms[i], lengths[j])))
            # Append the "runs" runtimes on OneMax
            results[i].append(run_parallel(runs, lengths[j],
                                           evolutionary_algorithms[i],
                                           default_parameters(evolutionary_algorithms[i], lengths[j]),
                                           OneMax,
                                           default_parameters(OneMax, lengths[j]),
                                           nb_cores))
            means[i].append(round(results[i][j].mean(), 2))

        print(header)
        for k in range(runs):
            line = ""
            for j in range(len(lengths)):
                line += str(results[i][j][k]) + ";"
            print(line)

    if excel == "True":
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        if not os.path.exists("export"):
            os.mkdir("export")
        if not os.path.exists("export/script_1"):
            os.mkdir("export/script_1")

        writer = pd.ExcelWriter(f"export/script_1/"
                                f"{start_length}_{end_length}_{length_step}_{runs}.xlsx", engine="xlsxwriter")
        # Write all the results in an Excel file
        for i in range(len(results)):
            df = pd.DataFrame()
            for j in range(len(lengths)):
                df[str(lengths[j])] = results[i][j]
            df.to_excel(writer, sheet_name=evolutionary_algorithms[i].name, index=True)

        # Add a sheet with the means
        df = pd.DataFrame({"Problem size": lengths})
        for i in range(len(evolutionary_algorithms)):
            df[evolutionary_algorithms[i].name] = means[i]
        df.to_excel(writer, sheet_name="Means", index=False)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()


# Evaluate cGA on OneMax with different values for K
def script_1_2(start_length, end_length, length_step, runs, nb_cores, excel):
    coefs = [1, 25, 125, 625, 3125, 15625]

    # Create array with all the length analysed
    lengths = []
    for iteration in range(start_length, end_length + 1, length_step):
        lengths.append(iteration)

    parameters = []
    for i in range(len(coefs)):
        parameters.append([])
        for length in lengths:
            parameters[i].append(math.ceil(coefs[i]*math.sqrt(length) * math.log(length)))

    results = []
    for i in range(len(coefs)):
        results.append([])
        header = ""
        sub_header = ""
        print("Coefficient: " + str(coefs[i]))
        for j in range(len(lengths)):
            header += evolutionary_algorithms[9].name + " " + str(lengths[j]) + ";"
            # Append the "runs" runtimes on OneMax
            update_cga = evolutionary_algorithms[9]
            sub_header += str(parameters[i][j]) + ";"
            update_cga.parameters[0].default_value = parameters[i][j]
            results[i].append(run_parallel(runs, lengths[j],
                                           update_cga,
                                           default_parameters(update_cga, lengths[j]),
                                           OneMax,
                                           default_parameters(OneMax, lengths[j]),
                                           nb_cores))
        print(sub_header)
        print(header)
        for k in range(runs):
            line = ""
            for j in range(len(lengths)):
                line += str(results[i][j][k]) + ";"
            print(line)


# Evaluate one algorithm on a fitness function
def script_2(evolutionary, fitness,
             start_length, end_length, length_step, runs, nb_cores, excel):
    print(evolutionary.name)
    print(fitness.name)
    # Create array with all the length analysed
    lengths = []
    for iteration in range(start_length, end_length + 1, length_step):
        lengths.append(iteration)

    results = []
    # For each algorithm and each length, run the algorithm "runs" time
    header = ""
    for j in range(len(lengths)):
        header += evolutionary.name + " " + str(lengths[j]) + ";"
        # Append the "runs" runtimes on OneMax
        results.append(run_parallel(runs, lengths[j],
                                    evolutionary,
                                    default_parameters(evolutionary, lengths[j]),
                                    fitness,
                                    default_parameters(fitness, lengths[j]),
                                    nb_cores))

    print(header)
    for k in range(runs):
        line = ""
        for j in range(len(lengths)):
            line += str(results[j][k]) + ";"
        print(line)


def script_2_1(index, start_length, end_length, length_step, runs, nb_cores, excel):
    algorithms = [(OnePlusOne, [4]),
                  (SDOnePlusOne, ["size^3"]),
                  (SAOneLambda, [10, 2, 2]),
                  (SDRLSR, ["size^3"])]

    for i in range(len(algorithms[index][1])):
        algorithms[index][0].parameters[i].default_value = algorithms[index][1][i]

    script_2(algorithms[index][0], JumpM,
             start_length, end_length, length_step, runs, nb_cores, excel)


def script_2_2(index_algorithm, index_fitness, start_length, end_length, length_step, runs, nb_cores, excel):
    algorithms = [(cGA, ["sqrt*log"])]
    functions = [(JumpOffsetM, [4]),
                 (JumpOffsetSpikeM, [4]),
                 (JumpOffsetSpikeM, [8])]

    for i in range(len(algorithms[index_algorithm][1])):
        algorithms[index_algorithm][0].parameters[i].default_value = algorithms[index_algorithm][1][i]

    for i in range(len(functions[index_fitness][1])):
        functions[index_fitness][0].parameters[i].default_value = functions[index_fitness][1][i]

    script_2(algorithms[index_algorithm][0], functions[index_fitness][0],
             start_length, end_length, length_step, runs, nb_cores, excel)




