# flume
Flume Related Data

The P-SAT folder contains a basic working example of the P-SAT Module.

Source Input files (keep in the same folder as the source *.py files) 
1.5_cm20140612010128.dat
1_cm20140612005538.dat

Ensure that the input_files.txt and input_files_corresponding_depths.txt are correspondingly filled. 

For ensemble_module, ensure that the csv filename is mentioned in the input_ensemble_files.txt

Execution Steps

1. Ensure Python 3 is installed 
2. If execution on Windows terminal :
python pots_module.py
python ensemble_module.py

3. If execution on Unix/Mac terminal :
python3 pots_module.py
python3 ensemble_module.py

After execution of the program, check the Filtered* folder containing the detailed analysis.