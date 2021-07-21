import time as t
import numpy as np
import os
import math

initial_t = t.time()

#Constraints
delta_ep = 3.0
delta_wl = 210.0 #armstrong 



file_path = "ultimate_list_2_r" #defines the line file that we want to analyse

#this functiont receives a line of the file and returns the respective wave length and excitation potential associated, it is assumed that the first number is the wave length and the tirth number is the excitation potential
def get_WL_EP(line):
	#defines the eposition of the required parameters on the line, count starts at 0 (zero)
	wl_n = 0
	ep_n = 2
	line = line.split()
	return line[wl_n], line[ep_n]


file = open(file_path, "r")
file_lines = file.readlines()
file.close()
file_lines = np.asarray(file_lines)

nol = len(file_lines)-1 #number of lines - nol

#2 dimensional array with the line and corresponding line wl and ep
lines = np.zeros([nol,2]) #the firts column corresponds to the wave lenght and the second to the excitation potential

for i in range(1,nol): #shift - first line to be ignored
	a = file_lines[i]
	wl,ep = get_WL_EP(a)
	lines[i-1,0],lines[i-1,1] = wl,ep


nop = 0 #number of pairs

#generated files names
file2_name = "Line Pairs Readable_" + str(delta_wl) + "_" + str(delta_ep)
file3_name = "Line Pairs_" + str(delta_wl) + "_" + str(delta_ep)

file2 = open(file2_name, "w")
file3 = open(file3_name, "w")

#set up the first line of the file
file2.write("Constraints: <" + str(delta_wl) + " >" + str(delta_ep) + " \n")
file3.write("Constraints: <" + str(delta_wl) + " >" + str(delta_ep) + " \n")

for i in range(0,nol):
	wl_1 = lines[i,0]
	for k in range(i+1,nol): #the plus 1 is because we dont want to pair line i with line i
		wl_2 = lines[k,0]
		dif_ep = round(abs(lines[i,1]-lines[k,1]),2)
		dif_wl = round(abs(wl_1-wl_2),2)
		if (dif_ep >= delta_ep) and (dif_wl<=delta_wl): #we pair up
			nop += 1
			#writes on file2 with the wanted format
			file2.write(str(wl_1) + " ")
			file2.write(str(wl_2) + " ")
			file2.write(str(dif_wl) + " ")
			file2.write(str(dif_ep) + " \n")
			#write on file3 with the wanted format
			file3.write(str(i) + " ")
			file3.write(str(k) + " \n")

file2.close()
file3.close()


print("Number of generated line pairs: " + str(nop) + "	Number of maximum line pairs: " + str(math.factorial(nol)/(2*(math.factorial(nol-2)))))
print("Execution time: " + str(round((t.time()-initial_t)*1000)) + " ms")
