import numpy as np
import os


def calculate_line_ratio(l1,l2):
	wl1 = l1[0]
	ew1 = l1[1]
	wl2 = l2[0]
	ew2 = l2[1]
	if wl1 > wl2:
		return ew1/ew2
	else:
		return ew2/ew1


#defined functions
def poly3(x,c0,c1,c2,c3): #degree 3 polynomial
	return c0 + c1*x + c2*x**2 + c3*x**3
def error_poly3(x,error_x,c1,c2,c3):
	return (c1+2*c2*x + 3*c3*x**2)*error_x

def poly1(x,c0,c1):
	return c0 + c1*x

def hiperbolic(x,c0,c1,c2): #hiperbolic function
	return c0/(x+c1) + c2

def remove_data_ew(data,ew_min, ew_max):
	col = len(data[0])
	lines = len(data[:,0])
	#elements to remove
	index1 = np.where(data[:,0]<=ew_min)
	index2 = np.where(data[:,0]>=ew_max)
	index3 = np.where(data[:,1]<=ew_min)
	index4 = np.where(data[:,1]>=ew_max)

	index = np.unique(np.append(np.append(np.append(index1,index2),index3),index4))
	nord = len(index) #number of removed data
	data_r = np.zeros([nord,col])
	data_1 = np.zeros([lines-nord,col])
	for i in range(col):
		for k in range(nord):
			data_r[:,i][k] = data[:,i][index[k]]
		data_1[:,i] = np.delete(data[:,i],index)
	return data_1, data_r


def remove_data(data, pos, r_min, r_max): #the positions refers to the data to remove 2-6 LR, temp, logg, met, mT
	col = len(data[0])
	lines = len(data[:,0])
	#elements to remove
	index1 = np.where(data[:,pos]<r_min)
	index2 = np.where(data[:,pos]>r_max)

	index = np.unique(np.append(index1,index2))
	nord = len(index) #number of removed data
	data_r = np.zeros([nord,col])
	data_1 = np.zeros([lines-nord,col])
	for i in range(col):
		for k in range(nord):
			data_r[:,i][k] = data[:,i][index[k]]
		data_1[:,i] = np.delete(data[:,i],index)
	return data_1

def remove_char(array,char = "\n"):#to be used with the reading of files
	for i in range(len(array)):
		array[i] = array[i].replace(char,"")#removes the newline character from the string in order to have the corrext name to open the documment
	return array

def get_settings(filename):
	options_file = open(filename,'r')
	options = remove_char(options_file.readlines())
	options_file.close()

	try:
		for i in range(len(options)):
			options[i] = options[i].split()[1]
	except IndexError:
		print("Error: Invalid options file formatting.")
		KeyboardInterrupt
	return options


def get_data(filename):
	temp_file = open(filename, 'r')
	data = np.asarray(temp_file.readlines())
	output = []
	output.append(float(data[3].split()[1].replace('\n',''))) #std
	output.append(float(data[0].split()[2].replace('\n',''))) #line1
	output.append(float(data[1].split()[2].replace('\n',''))) #line2
	output.append(float(data[4].split()[1].replace('\n',''))) #C0
	output.append(float(data[5].split()[1].replace('\n',''))) #C1
	output.append(float(data[6].split()[1].replace('\n',''))) #C2
	output.append(float(data[7].split()[1].replace('\n',''))) #C3
	output.append(int(data[2].split()[1].replace('\n','')))   #flag
	return output


def get_ares_data(filepath):
	file_data = np.loadtxt(filepath,dtype=float)
	processed_data = np.zeros([len(file_data),3],dtype=float)
	processed_data[:,0] = file_data[:,0] #wave length
	processed_data[:,1] = file_data[:,4] #equivalent width
	processed_data[:,2] = file_data[:,5] #ew error
	return processed_data

def get_LR_data(filepath):
	file_data = np.loadtxt(filepath,dtype=float,usecols=(0,1,2,3,4,5,6,7,8),skiprows=1)
	return file_data

def calculate_LR_error(l1,l2,flag):
	wl1 = l1[0]
	ew1 = l1[1]
	error1 = l1[2]
	wl2 = l2[0]
	ew2 = l2[1]
	error2 = l2[2]
	if wl1 > wl2:
		return np.sqrt((1/ew2**2)*error1**2 + (ew1/ew2**2)**2*error2**2)
	else:
		return np.sqrt((1/ew1**2)*error2**2 + (ew2/ew1**2)**2*error1**2)

def calculate_average_and_error(values, values_error):
	w = (1/values_error**2)/np.sum(1/values_error**2)
	mean = np.average(values, weights = w)
	error = np.sqrt(np.average((values-mean)**2, weights=w))
	return mean, error


def get_compare_file_data(filepath):
	data = np.loadtxt(filepath, skiprows=1,usecols = (2,4,5,8,9,10,11,17)) #std, line1, line2, c0,c1,c2,c3
	return data

def get_pairs(file_path):
	data = np.loadtxt(file_path)
	return data

def get_data_TMCalc(file_path,nop):
	data = np.loadtxt(file_path)
	temps = data[0:nop,0]
	stds = data[0:nop,1]
	return temps,stds, data[-1,0], data[-1,1]

def test_compile(path,files_names,nop,nof):
	array_old = np.loadtxt(path + files_names[0],usecols = (0,1),dtype=np.float32)

	for i in range(1,nof):
		array = np.loadtxt(path + files_names[i],usecols = (0,1),dtype=np.float32)
		comparinson = (array_old == array).all()
		if not comparinson:
			print('Testing as failed.')
			KeyboardInterrupt
		else:
			array_old = np.copy(array)
		np.savetxt(path + 'pairs',array)

	print('Testing sucessfull! No error found.')

	return 0
