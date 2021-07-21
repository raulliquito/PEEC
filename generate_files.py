#Python 3 program
import numpy as np
import os
import time as t

initial_t = t.time()

#microturbulence
mT = 1.0
#we set the intervals for all the parameters and the associated step (for later use on the for loops)

#Temperature-Kelvin
temp_i = 4000.0
temp_f = 8000.0
temp_step = 25
n_temp = int((temp_f-temp_i)/temp_step)

#Logg
logg_i = 1.0
logg_f = 5.0
logg_step = 0.1
n_logg = int((logg_f-logg_i)/logg_step)

#[Fe/H] dex
met_i = -1.0
met_f = 0.5
met_step = 0.1 #0.25
n_met = int((met_f-met_i)/met_step)

temp_l = np.linspace(temp_i,temp_f,n_temp+1)
logg_l = np.linspace(logg_i,logg_f,n_logg+1)
met_l = np.linspace(met_i,met_f,n_met+1)

os.system("rm MOOG_render/*")

nof = 0 #number of files (nof)  iteration counter
nameof = np.array([],str) #numpy array that holds all the name files, later used to check the files

for i in range(len(temp_l)): #runs trough all the temperatures
	temp = round(temp_l[i],3)
	for j in range(len(logg_l)): #runs trough all the logg's
		logg = round(logg_l[j],3)
		for k in range(len(met_l)): #runs trough all met's
			met = round(met_l[k],3)
			nof += 1
			#runs interpolation algorithm for atmosferic input MOOG file and 				then runs MOOG with the new file
			os.system("bash ~/Desktop/MOOG/interpol_models_marcs/make_model_marcs.bash "+str(temp) + " " + str(logg) + " " + str(met) + " " + str(mT))
			os.system("~/Desktop/MOOG/MOOG2019/MOOGSILENT")
			filename = str(temp) + "_" + str(logg) + "_" + str(met) + "_" + str(mT) + ".test"
			os.system("mv ew_test.test " + filename) #renames the MOOG output file
			os.system("mv " + filename + " MOOG_render/") #moves the renamed file into MOOG_render dir
			nameof = np.append(nameof,filename)


#=============Check files===============
#the intent of this program is to check wich files outputted correct information vs wich ones didnt and delete the useless files. Returns the number of cleared files
nodf = 0 #number of deleted files
file2 = open("MOOG_render/files_name", "w")#file that stores the name of all the generated usefull files

for i in range(nof):
	file_path = "MOOG_render/"+nameof[i]
	file = open(file_path, "r")
	line = file.readline()
	if  line == "": #empty file
		os.system("rm " + file_path) #deletes file
		nodf += 1
	else:
		file2.write(nameof[i])
		file2.write("\n")
	file.close()
file2.close()



os.system("rm a out_marcs.atm interpol_moog.com")

print("MOOG generated " + str(nof) + " files. " + str(nodf) + " were deleted. " + str(nof-nodf) + " files remaining.\n")
print("Execution time: " + str((t.time()-initial_t)/60) + " minutes.")
