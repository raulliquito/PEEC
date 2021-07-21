import numpy as np
import time as t

#This script restructures the input line file so it is accepted by MOOG

list_filename = 'ultimate_list_2'


try:
	data = np.loadtxt(list_filename, dtype = str,skiprows = 1,usecols = (0,1,2,4,5))
except IOError:
	print('Invalid File Name. Try again.')
else:
	wl, ex, logg, num, ew = data[:,0], data[:,1], data[:,2], data[:,3], data[:,4]
	
	file = open(list_filename + '_r', 'w')
	file.write(' running_dir/' + list_filename + '\n')
	for i in range(len(wl)):
		line = str(wl[i]).rjust(9)+ str(num[i]).rjust(8) + str(ex[i]).rjust(12) + str(logg[i]).rjust(11) + str(ew[i]).rjust(28) + '\n'
		file.write(line)
	
	file.close()

	

