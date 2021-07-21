import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sco
import time as t
import os
import progress.bar as pb
from functions import *

t_i = t.time()

#=======================================================================================================================================================================

#clears directories
print("\n====================================================================\n")
print("For this scrip ignore any RuntimeWarning regarding overflow.")
print("\n====================================================================\n")

#this program is modular, in order to change the ouput and constraints interval, open and change the options file. (More info in README)
options = get_settings('options')

#set the options according to file
nop = int(options[0])
fig_extension = options[1].lower()
dir_op = options[2].lower()
save_folder = options[3]
colorbar_status = options[4].lower()
ew_min = float(options[5])
ew_max = float(options[6])
rm_logg = options[7].lower()
logg_min = float(options[8])
logg_max = float(options[9])
rm_temp = options[10].lower()
temp_min = float(options[11])
temp_max = float(options[12])
add_on = options[13].lower()

#=======================================================================================================================================================================
#=======================================================================================================================================================================
if add_on == 'ew':
	cmd1 = 'fig, (ax11,ax12) = plt.subplots(1, 2,figsize = (16,8))'
	cmd2 = ("ax12.scatter(ew1,temp2,s=5,label = 'Data Points EW1')\n"
		"ax12.scatter(ew2,temp2,s=5,label = 'Data Points EW2')\n"
		"ax12.scatter(ew1_r,temp_r,s=5,color = 'k',label = 'Data Points EW1')\n"
		"ax12.scatter(ew2_r,temp_r,s=5,color = 'k',label = 'Data Points EW2')\n"
		"ax12.vlines([ew_min,ew_max],np.amin(temp)-200,np.amax(temp)+200,linestyle = 'dashed')\n"
		"ax12.legend()\n"
		"ax12.set_xlabel('EW')\n"
		"ax12.set_ylabel('Temperature (k)')\n"
		"ax12.set_ylim(np.amin(temp)-200,np.amax(temp)+200)\n"
		"ax12.grid()\n")
else:
	cmd1 = 'fig, (ax11) = plt.subplots(1, 1,figsize = (16,8))'
	cmd2 = 'None'#does nothing


if dir_op == 'rm':
	os.system("rm -f ~/generate_models/" + save_folder + "/Optimal_STD/*")
	os.system("rm -f ~/generate_models/" + save_folder + "/Low_STD/*")
	os.system("rm -f ~/generate_models/" + save_folder + "/Medium_STD/*")
	os.system("rm -f ~/generate_models/" + save_folder + "/High_STD/*")
	os.system("rm -f ~/generate_models/" + save_folder + "/Parameters/*")
elif dir_op == 'mk':
	os.system("mkdir -p ~/generate_models/" + save_folder)
	os.system("mkdir -p ~/generate_models/" + save_folder + "/Optimal_STD")
	os.system("mkdir -p ~/generate_models/" + save_folder + "/Low_STD")
	os.system("mkdir -p ~/generate_models/" + save_folder + "/Medium_STD")
	os.system("mkdir -p ~/generate_models/" + save_folder + "/High_STD")
	os.system("mkdir -p ~/generate_models/" + save_folder + "/Parameters")


#stores the ammount of optimal/low/mediu/high graphs generated
noog = 0
nolg = 0
nomg = 0
nohg = 0

error_counter = 0

#set progress bar

bar = pb.IncrementalBar('Progress', max = nop, suffix = '%(index)d/%(max)d')

for i in range(nop):
	#data maniulation
	header = np.loadtxt("line_pair_data/" + str(i),max_rows = 1)
	data = np.loadtxt("line_pair_data/" + str(i),skiprows = 1)

	if rm_logg == 'yes':
		data = remove_data(data,4,logg_min,logg_max)
	if rm_temp == 'yes':
		data = remove_data(data,3,temp_min,temp_max)
	if ew_min != ew_max: #if the values are the same the constraint is turned off
		data, data_r = remove_data_ew(data,ew_min,ew_max) #removes data under certain constrains

	ew1 = data[:,0]
	ew2 = data[:,1]
	LR = data[:,2]
	temp = data[:,3]
	logg = data[:,4]
	met = data[:,5]

	ew1_r = data_r[:,0]
	ew2_r = data_r[:,1]
	LR_r= data_r[:,2]
	temp_r = data_r[:,3]
	logg_r = data_r[:,4]
	met_r = data_r[:,5]

	#======================================

	adj_LR = np.linspace(0,np.amax(LR),2000)
	adj_LR_r = np.linspace(0,np.amax(1/LR),2000)
	adj_LR_log = np.linspace(np.amin(np.log10(LR)),np.amax(np.log10(LR)),2000)

	try:
		c,cov = sco.curve_fit(poly3,LR,temp)
		adj_temp = poly3(adj_LR,c[0],c[1],c[2],c[3])
		residues = temp - poly3(LR,c[0],c[1],c[2],c[3])
		sigma = np.std(residues,dtype=np.float64)

	except (RuntimeError, RuntimeWarning):
		sigma = 5000
		pass

	try:
		c_r,cov_r = sco.curve_fit(poly3,1/LR,temp)
		adj_temp_r = poly3(adj_LR_r,c_r[0],c_r[1],c_r[2],c_r[3])
		residues_r = temp - poly3(1/LR,c_r[0],c_r[1],c_r[2],c_r[3])
		sigma_r = np.std(residues_r,dtype=np.float64)

	except (RuntimeError, RuntimeWarning):
		sigma_r = 5000
		pass

	try:
		c_log,cov_log = sco.curve_fit(poly3,np.log10(LR),temp)
		adj_temp_log = poly3(adj_LR_log,c_log[0],c_log[1],c_log[2],c_log[3])
		residues_log = temp - poly3(np.log10(LR),c_log[0],c_log[1],c_log[2],c_log[3])
		sigma_log = np.std(residues_log,dtype=np.float64)

	except (RuntimeError, RuntimeWarning):
		sigma_log = 5000
		pass


	if sigma == min(sigma,sigma_r,sigma_log ):
		flag = 0 #the zero represents the normal line ratio
	elif sigma_r == min(sigma,sigma_r,sigma_log ):
		sigma = sigma_r
		c = c_r
		cov = cov_r
		adj_temp = adj_temp_r
		residues = residues_r
		flag = 1 #the one represents the inverted line ratio
	elif sigma_log == min(sigma,sigma_r,sigma_log ):
		sigma = sigma_log
		c = c_log
		cov = cov_log
		adj_temp = adj_temp_log
		residues = residues_log
		flag = 2 #the two represents the logarithm of the line ratio

	if flag == 1: #invert LR
		LR = 1/LR
		adj_LR = adj_LR_r
		x_axis_label = '1/(Line Ratio)'
	elif flag == 2:
		LR = np.log10(LR)
		adj_LR = adj_LR_log
		x_axis_label = 'Log(Line Ratio)'
	else:
		x_axis_label = 'Line Ratio'

	temp2 = np.copy(temp) # for the ew graph dont want to remove outliers

	#Remove outliers with 2*sigma constraint
	outliers = np.append(np.where(residues>2*sigma),np.where(residues<-2*sigma))
	LR_out = LR[outliers]
	temp_out = temp[outliers]
	logg_out = logg[outliers]
	met_out = met[outliers]
	residues_out = residues[outliers]

	LR = np.delete(LR,outliers)
	temp = np.delete(temp,outliers)
	logg = np.delete(logg,outliers)
	met = np.delete(met,outliers)
	residues = np.delete(residues,outliers)

	try:
		c1,cov1 = sco.curve_fit(poly3,LR,temp)
		adj_temp1 = poly3(adj_LR,c1[0],c1[1],c1[2],c1[3])
		fig_name_append = "  C0: " + str(c1[0])+ "  C1: " + str(c1[1])+ "  C2: " + str(c1[2])+ "  C3: " + str(c1[3])
	except (RuntimeError, RuntimeWarning):
		error_counter += 1
		continue

	if colorbar_status == 'logg':
		cb = logg
		cb_out = logg_out
		cb_label = 'Log(g)'
	elif colorbar_status == 'met':
		cb = met
		cb_out = met_out
		cb_label = 'Metalicitty'
	else:
		cb = 'orange'
		cb_out = 'black'
		cb_label = 'None'


	exec(cmd1) #executes the setted commadn depending on the add_on string
	title = "Graph " + str(i) + ": " + str(header[0]) + " " + str(header[1]) + "   σ: " + str(round(sigma))
	#ax11
	fig.suptitle(title + fig_name_append)
	s = ax11.scatter(LR,temp, s=7,c = cb,label = 'Data Points')
	s = ax11.scatter(LR_out,temp_out ,marker = "^" ,edgecolors='black',linewidths = 0.5, s=7,c = cb_out,label = 'Outliers')
	ax11.plot(adj_LR,adj_temp,'--',label = 'Old ' + 'Polinomial Fit Order: 3')
	ax11.plot(adj_LR,adj_temp1,linewidth = 1,label = 'Polinomial Fit Order: 3')
	ax11.plot(adj_LR,adj_temp-2*sigma,'k--',linewidth = 1)
	ax11.plot(adj_LR,adj_temp+2*sigma,'k--',linewidth = 1)
	ax11.legend()
	ax11.set_xlabel(x_axis_label)
	ax11.set_ylabel("Temperature (k)")
	ax11.set_ylim(np.amin(temp)-200,np.amax(temp)+200)
	ax11.grid()

	#ax12
	exec(cmd2)


	if cb_label != 'None':#colorbar
		plt.colorbar(s,ax = ax11,label = cb_label)

	name_of_fig = title + fig_extension

	#save data into parameter file
	name_of_file = str(i)
	parameter_file = open(save_folder + '/Parameters/' + name_of_file, 'w')

	parameter_file.write('Line 1:' + str(header[0]).rjust(25) + '\n')
	parameter_file.write('Line 2:' + str(header[1]).rjust(25) + '\n')
	parameter_file.write('  Flag:' + str(flag).rjust(25) + '\n')
	parameter_file.write('   STD:' + str(round(sigma)).rjust(25) + '\n')
	parameter_file.write('    C0:' + str(round(c1[0],3)).rjust(25) + '\n')
	parameter_file.write('    C1:' + str(round(c1[1],3)).rjust(25) + '\n')
	parameter_file.write('    C2:' + str(round(c1[2],3)).rjust(25) + '\n')
	parameter_file.write('    C3:' + str(round(c1[3],3)).rjust(25) + '\n')
	parameter_file.close()


	if sigma<200.0:
		fig.savefig(save_folder + "/Optimal_STD/" + name_of_fig,dpi = fig.dpi)
		noog += 1
	elif sigma<320.0 and sigma>200.0:
		fig.savefig(save_folder + "/Low_STD/" + name_of_fig,dpi = fig.dpi)
		nolg += 1
	elif sigma>450.0:
		fig.savefig(save_folder + "/High_STD/" + name_of_fig,dpi = fig.dpi)
		nohg += 1
	else:
		fig.savefig(save_folder + "/Medium_STD/" + name_of_fig,dpi = fig.dpi)
		nomg += 1
	plt.close()

	bar.next()

bar.finish()
#print(error_counter)
print("\nThe program generated " + str(noog) + " Optimal STD graphs, " + str(nolg) + " Low STD graphs, " + str(nomg) + " Medium STD graphs and " + str(nohg) + " High STD graphs.\n")
print("The number of errors obtained while finding optimal fit curve were: " + str(error_counter))
print("The execution time was " + str(round(t.time()-t_i)) + " seconds.")
