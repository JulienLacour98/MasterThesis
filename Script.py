import os.path
from Interface import *


# Evaluate all the algorithms on OneMax
def script_1(start_length, end_length, length_step, runs):
    # Create array with all the length analysed
    lengths = []
    for iteration in range(start_length, end_length + 1, length_step):
        lengths.append(iteration)

    results = []
    means = []
    # For each algorithm and each length, run the algorithm "runs" time
    for i in range(len(evolutionary_algorithms)):
        print(evolutionary_algorithms[i].name)
        results.append([])
        means.append([])
        for j in range(len(lengths)):
            print(lengths[j])
            # Append the "runs" runtimes on OneMax
            results[i].append(run_parallel(runs, lengths[j],
                                           evolutionary_algorithms[i],
                                           default_parameters(evolutionary_algorithms[i], lengths[j]),
                                           OneMax,
                                           default_parameters(OneMax, lengths[j])))
            means[i].append(round(results[i][j].mean(), 2))

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
    df = pd.DataFrame({"Lengths/Algorithms:": lengths})
    for i in range(len(evolutionary_algorithms)):
        df[evolutionary_algorithms[i].name] = means[i]
    df.to_excel(writer, sheet_name="Means", index=False)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
