import numpy as np
import time as t
import os
from functions import *

initial_t = t.time()
#ATTENTION: LINE RATIO IS DIFINED HAS THE EW OF THE BIGGER wl DIVIDING BY THE EW OF THE SMALLER wl
#nop = input('Input the number of avaiable pairs: ')
print('==================================================================================\n')
lpf = input('Input name/dir of line pair data (name type: Line Pairs_λ_χ): ')
print('\n')
print('==================================================================================\n')
#===================================================Functions===================================================

def remove_char(array,char = "\n"):#to be used with the reading of files
	for i in range(len(array)):
		array[i] = array[i].replace(char,"")#removes the newline character from the string in order to have the corrext name to open the documment
	return array

def generate_files(n,lp_readable): # n = number of files to generate, 1 file per line pair
	os.system('mkdir -p line_pair_data1')
	os.system("rm line_pair_data1/*")
	for i in range(n):
		file = open("line_pair_data1/" + str(i),"w")
		file.write(lp_readable[i] + '\n')
		file.close()
	return 0

def extract_MOOG_data(filepath): #extracts the EWcalc values from the MOOG file
	file = open(filepath, "r")
	data = remove_char(np.asarray(file.readlines())[5:])
	file.close()
	l = len(data)
	ew = np.zeros([l,2])
	for i in range(l):
		line = np.asarray(data[i].split())
		ew[i,0] = float(line[0])
		ew[i,1] = float(line[-1])
	return ew

def get_params(filename):
	filename = filename.replace(".test","").split("_")
	temp,logg,met,mT = float(filename[0]),float(filename[1]),float(filename[2]),float(filename[3])
	return temp, logg, met, mT


#===============================================================================================================


#here we extract all the names of the files we will need to read and store it in a numpy array
file = open("MOOG_render/files_name", "r")
files_name = file.readlines()
files_name = np.asarray(files_name)
file.close()
files_name = remove_char(files_name)
nof = len(files_name)


#here we want to extract the line pairs into a usable data structure
file = open(lpf,"r")
file1 = open(lpf[:10] + " Readable"  +lpf[10:],"r")
line_pairs_1 = file1.readlines()
line_pairs = file.readlines()
file1.close()
file.close()
line_pairs = remove_char(np.asarray(line_pairs)[1:]) #converts into numpy array, excludes first line of the file and removes newline char
line_pairs_1 = remove_char(np.asarray(line_pairs_1)[1:])
nop = len(line_pairs)

generate_files(nop,line_pairs_1)#generates the files where the analysis date will be saved

noe = 0

for k in range(nof):#goes through all the MOOG generated files
	name = files_name[k]
	MOOG_data = extract_MOOG_data("MOOG_render/" + name)
	temp,logg,met,mT = get_params(name)
	for i in range(nop): #goes through all the pairs on the list
		pair = np.asarray(line_pairs[i].split(),dtype = int)
		try:
			l1, l2 = MOOG_data[pair[0]], MOOG_data[pair[1]]
		except IndexError:
			print("Error Ocurred at " + name + '\n')
			noe += 1
			break
		file = open("line_pair_data1/" + str(i),"a")
		line = str(l1[1]) + ' ' + str(l2[1]) + ' ' + str(calculate_line_ratio(l1,l2)) + " " + str(temp) + " " + str(logg) + " " + str(met) + " " + str(mT) + "\n"
		file.write(line)
		file.close()


print("\n")
print("The program ended!")
print('The total ammount of error were: ' + str(noe) + '.')
print("The execution time was " + str(round((t.time()-initial_t),2)) + " seconds.")
