# PEEC
Calculating Teff of warm stars using equivalent widths line ratios


To generate all the models and feed them to MOOG run the command:

$	python3 generate_files.py

To analyse and compile all the line pairs according to the wanted constraints run command:

$	python3 generate_line_pairs.py

===========================generate_files.py============================

The interpolation algorithm generates a out_marcs.atm, MOOG takes this new file in. This code requires to be ran from a specific dir, the one used is:

$	/home/raulliquito/generate_models/

On the generate_models folder it is needed a batch.par file with the correct paths and options, line 1: ewfind, line 12: /home/raulliquito/generate_models/out_marcs.atm
It is also needed a line sample file that needs to be in the same dir.

MOOG output file is ew_test.test, however the code stores the generated files in a second dir (MOOG_render) with the following name:

temperature_logg_metalicitty_microturbulence.test 	example: 5684_4.5_1.0_1.0.test

ATTENTION: EVERYTIME THE CODE RUNS ALL THE FILES INSIDE MOOG_render DIR ARE DELETED.

If the paths/dir's are changed, the path in line 32 os.system("rm MOOG_render/*") needs to be updated, it is also possible to comment the line typing the character # in the beginning of the line.

After all the files are generated by MOOG, the program will then scan all the files, any empty file will be deleted. At the same time the program generates a new file on MOOG_render dir called files_name that stores in each line the name of all the remaining files.

The final output of the program is:
	-all the usefull MOOG generated files
	-file with the name of all generated files
	-the number of original files generated
	-the number of deleted files
	-the number of final files
	-the execution time


===========================generate_line_pairs.py============================
ATTENTION: The line file needs to be in the correct form check restructure.py.

In case the line file to analyse is changed either in name, dir or both the path on line 5 needs to be changed to the correct file path.

The get_WL_EP function receives a line of the file and returns the respective wave length and excitation potential associated. It is assumed that the first number is the wave length and the tirth number is the excitation potential. If the file type changes the funtion needs to be equally changed to meet the new requirements.

This program uses several restraints to for line pairing. These constrains are set on the beginning of the program, tagged as such. This constrains can be changed on the beginning of the program. In case more constraints need to be added the the code will need to be adapted  on line 60 in order to test the new constraints.

This program outputs 2 text files, each one with the same information. The first one is called /Line Pairs Readable_(...)_(...), it's structure is the following:

$1: Constraints: <Δλ >Δχ
$n: λ1 λ2 Δλ Δχ

Each line corresponds to a line pair.
The second one is called /Line Pairs_(...)_(...), it's structure is the following:

$1: Constraints: <Δλ >Δχ
$2: #λ1 #λ2
$n: #λ1 #λ7

#λ3 represents the positional number of the line in the original file so it becomes easier for the computer to analyse the line pairs and extract them from the corresponding MOOG generated file.

ATTENTION: EVERYTIME THE CODE RUNS BOTH THE GENERATED FILES ARE DELETED.

The final output of the program is:
	-two files each one containning the information regarding the line pairing done
	-the maximum number o possible pairs generated
	-the number of pairs generated
	-the execution time

==========================restructure.py===============================

This script receives a line file and outputs a new file with the correct formatting. It's important to note that each value extractions dependes on the input file set on line 6.

The output file has the following structure:

#1: running dir/(name of file)
#n:   wl num logg wl

With the correct spacing between columns.

The final output of the program is:
	-one file with the explained structure
	-the execution time
===========================generate_LR_vs_temp.py==============================

This script generates the necessary data, calculating the Line Ratio has defined on the script.

ATTENTION: EVERYTIME THE CODE RUNS THE line_pair_data DIR IS FORMATED

In case the folder does not exist, it will be created on the running dir.

This script generates a number of files equal to the total line pairs. Each file corresponds to the grouping of all the data that corresponds to a particular line pair. The structure of the file is:

#1: wl1 wl2
#n: ew1 ew2 LR temp logg met mT

The final output of the program is:
	-N files of all the analysed data
	-new DIR
	-the execution time
