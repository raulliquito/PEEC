import numpy as np
import time as t
import progress.bar as pb
from functions import *
import matplotlib.pyplot as plt
import os

def main(lr_data_file_path,ares_file_path,tmcalc_output):
	print('-Running script for ' + ares_file_path.split('/')[-1])

	ares_data = get_ares_data(ares_file_path)
	lr_data = get_LR_data(lr_data_file_path)

	nop = len(lr_data[:,0])


	bar = pb.IncrementalBar('No. of Analysed Line Pairs', max = nop, suffix = '%(index)d/%(max)d')

	temps = np.array([],dtype=np.float32)
	#temps_errors = np.array([],dtype=np.float32)
	temps_errors_1 =np.array([],dtype=np.float32)

	star_name = ares_file_path.split('/')[-1].split('.')[0]
	output_file = open('TMCalc_Output_Data/' + star_name + '.temperatures', 'w')
	np.savetxt('TMCalc_Output_Data/' + star_name + '.pairs', lr_data[:,2:4])


	for i in range(nop): #goes through each line pair on lr_data_file and searches htough the ares output file
		bar.next()
		pair_data = lr_data[i]

		std = pair_data[1]
		flag = pair_data[8]#defines the used line ratio

		line1 = pair_data[2]
		line2 = pair_data[3]

		#write line pair to file
		#output_file_1.write(str(line1).rjust(11) + str(line2).rjust(11) + '-1'.rjust(11) + '-1'.rjust(11) + '\n' )

		line1_pos = np.where(ares_data[:,0]==line1)[0] #gets de position of the line1 on the ares file, its an array the position is the firts entry
		line2_pos = np.where(ares_data[:,0]==line2)[0] #gets the posiotion of line2 on the ares file, its an array the position is the firts entry
		#need to test if poth lines exist

		if len(line1_pos)==0 or len(line2_pos)==0:
			output_file.write('-1'.rjust(10) + '-1'.rjust(7) + '\n')
			continue

		#save the useful data, pos: 0-wl 1-ew 2-ew_error
		l1 = np.zeros(3,int)
		l1[0],l1[1],l1[2] = ares_data[line1_pos[0]]
		l2 = np.zeros(3,int)
		l2[0],l2[1],l2[2] = ares_data[line2_pos[0]]
		#calculate Line Ratio, defined has the ew of the bigger wave lenght dividing by the ew of the samallest wave length
		lr = np.array([calculate_line_ratio(l1,l2),abs(calculate_LR_error(l1,l2,flag))],dtype=np.float32)

		if flag == 1:
			lr[1] = abs(lr[1]/lr[0]**2)
			lr[0] = 1/lr[0]
		elif flag == 2:
			lr[1] = abs(lr[1]/(lr[0]*np.log(10)))
			lr[0] = np.log10(lr[0])
		#use fit to estimate temperature with this pair
		coefs = pair_data[4:8]
		temp_estimate = poly3(lr[0],coefs[0],coefs[1],coefs[2],coefs[3])

		output_file.write(str(round(temp_estimate,3)).rjust(10)  + str(std).rjust(7) + '\n')
		#temp_error = abs(error_poly3(lr[0],lr[1],coefs[1],coefs[2],coefs[3]))
		#if temp_error == 0:
		#	bar.next()
		#	continue

		if (temp_estimate >= 4000 and temp_estimate <= 12000):
			temps = np.append(temps,temp_estimate)
			#temps_errors = np.append(temps_errors,temp_error)
			temps_errors_1 = np.append(temps_errors_1,std)
		else:
			continue


	bar.finish()

	#mean, error = calculate_average_and_error(temps,temps_errors)
	mean_1, error_1 = calculate_average_and_error(temps,temps_errors_1)
	nopu_1 = len(temps) #nopu = number of pairs used

	#remove outliers with 2 sigma enquadration
	residues = temps-mean_1
	outliers = np.where(abs(residues)>2*temps_errors_1)
	temps = np.delete(temps,outliers)
	temps_errors_1 = np.delete(temps_errors_1,outliers)
	mean_1_r, error_1_r = calculate_average_and_error(temps,temps_errors_1)
	nopu_1_r = len(temps)

	output_file.write(str(round(mean_1_r,4)) + '  ' + str(round(error_1_r,4)))
	#output_file_1.close()
	output_file.close()

	if tmcalc_output == 'yes':
		print('\nTmCalc output is: \n')
		os.system(' bash ../TMCALC-master/TMCalc.bash ' + ares_file_path)
		print('\n')
	print('\nAssuming fit STD, this program output is:')
	#print('Teff: ' + str(round(mean,4)) + ' +/- ' + str(round(error,4)) + '  assuming error propagation.')
	print('Teff: ' + str(round(mean_1,4)) + ' +/- ' + str(round(error_1,4)) + '  without outlier removal (' + str(nopu_1) + ').')
	print('Teff: ' + str(round(mean_1_r,4)) + ' +/- ' + str(round(error_1_r,4)) + '  with outlier removal (' + str(nopu_1_r) + ').' + '\n\n\n')


# Temps graphs and respective weighted mean
	#plt.figure(1,figsize=(16,8))
	#plt.plot(temps,'k.', label = 'Temperatures')
	#plt.hlines(mean_1,0,len(temps), label = 'Mean')
	#plt.hlines(mean_1_r,0,len(temps),'orange', label = 'Mean 1')
	#plt.legend()
	#plt.grid()
	#plt.show()

	return 0


options = get_settings('options_TMCalc')

lr_data_file_path = options[0]
ares_file_path = options[1]
tmcalc_output = options[2].lower()
run_several_files = options[3].lower()
ares_several_files_path = options[4]

os.system('clear')

print('===========================================================================================================================\n')
print('                  For this Temperature estimation it was assumed that there is no correlation between line pairs.          \n')
print('                                   Running dir: ' + lr_data_file_path + '\n')
print('===========================================================================================================================\n\n')

if run_several_files == 'yes':
	file_path = ares_several_files_path
	file_name = 'files'

	try:
		file = open(file_path + file_name,'r')
	except IOError:
		print('Invalid File Path/Name')
		KeyboardInterrupt

	files_names = remove_char(file.readlines())
	for i in range(len(files_names)):
		file_path + files_names[i]
		main(lr_data_file_path,file_path + files_names[i],tmcalc_output)

else:
	main(lr_data_file_path,ares_file_path,tmcalc_output)
