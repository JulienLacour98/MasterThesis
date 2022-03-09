# MasterThesis
Implementation and Evaluation of Strategies for Escaping Local Optima with Evolutionary Algorithms


# Libraries
The following libraries need to be imported:
- matplotlib
- numpy
- openpyxl
- pandas
- XlsxWriter

# Exports / Imports
- All exported data will be found in the folder "export" and sorted in an action folder
  - Data exported from a script "i" will be in the folder "export/script_i" where the name file is the parameters used. Using the same parameters again will erase the previous run. 
  - Data exported from the interface within an "action" will be under the folder "export/interface/action" and will have the data as a name file.
- Importing file is not possible at the moment

# Running the framework
- In order to run the framework use the following command in the terminal: "python3 Main.py [script] [params]" with:
  - [script] in [0, 1]: 
    - 0 to display the interface. [param] is then empty.
    - 1 to start the first script to run all the functions on OneMax. [params] is then [start_length] [end_length] [length_step] [runs] [cores] [hpc] with:
      - [start_length]: Starting problem size (integer)
      - [end_length]: Ending problem size (integer)
      - [length_step]: Gap between each problem size that is analysed (integer)
      - [runs]: Number of iterations per problem size (integer)
      - [cores]: Number of cores used for running the algorithm (integer)
      - [generate_excel]: 1 if you want an Excel to be generated. Not possible on the HPC of DTU. (integer)