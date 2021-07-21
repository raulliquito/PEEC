import numpy as np
import matplotlib.pyplot as plt
from functions import *

#set options
options = get_settings('options_analyse_TMCalc')
working_dir = options[0] #TMCalc output data dir
data_dir = options[1]
show_graph = options[2].lower()
valid_fits_interval = abs(float(options[3]))
max_std_value = abs(float(options[4]))

SweetCat_temperatures = np.array([6732,6403,6251,6510,6361,6301,6374,6136,6158,6503])

#get stars names
data = open(working_dir+data_dir+'files_temperatures')
files_names = np.asarray(remove_char(data.readlines()))
data.close()
nof = len(files_names)

data = open(working_dir+data_dir+'files_pairs')
files_names_func = np.asarray(remove_char(data.readlines()))
data.close()


#number of pairs
temporary = open(working_dir + data_dir + files_names[0],'r')
nop = len(temporary.readlines())-1
temporary.close()

test_compile(working_dir+data_dir, files_names_func,nop,nof)

line_pairs = get_pairs(working_dir+data_dir+'pairs')

#set data structure and built it

temperature_data = np.zeros([nop,nof])
std_data = np.zeros([nop,nof])

desvios_medios = np.zeros(nop)
std_desvios_medios = np.zeros(nop)
std_fit = np.zeros(nop)
flags = np.zeros(nop)
faulty_pairs_index = np.array([])

for i in range(nof): #goes trhough all the star files data
    temps, stds , star_temp, temp_std = get_data_TMCalc(working_dir+data_dir+files_names[i],nop)
    temps -= SweetCat_temperatures[i]
    #calculate temperature deviation
    temperature_data[:,i] = temps #sets the temperature deviation
    std_data[:,i] = stds #set the std

for i in range(nop):
    error_data = std_data[i]
    plot_data = temperature_data[i]
    delete_index = np.where(abs(plot_data)>1000)[0]


    flag = len(delete_index)

    if flag == 0:
        desvios_medios[i] = np.average(plot_data)
        std_desvios_medios[i] = np.std(plot_data)
        std_fit[i] = stds[0]
    elif flag == nop: #checks if there is pairs that didnt calculate a single temperature for all the given stars
        faulty_pairs_index = np.append(faulty_pairs,i)
    else:
        desvios_medios[i] = np.average(np.delete(plot_data,delete_index))
        std_desvios_medios[i] = np.std(np.delete(plot_data,delete_index))
        std_fit[i] = np.delete(stds,delete_index)[0]



    #plt.figure(i,figsize = (16,8))
    #title = str(round(line_pairs[i,0],2)) + '   ' + str(round(line_pairs[i,1],2)) + '    STD: ' + str(round(pair_std,2)) + '  Flag: ' + str(flag)
    #x = np.arange(1,len(plot_data)+1,1)

    #plt.title(title)
    #plt.errorbar(x,plot_data, error_data,np.zeros(12),'o')
    #plt.grid()
    #plt.show()
    #plt.close()
#need to remove all the faulty_pairs data_dir

if len(faulty_pairs_index) !=0:
    desvios_medios = np.delete(desvios_medios,faulty_pairs_index)
    std_desvios_medios = np.delete(std_desvios_medios,faulty_pairs_index)
    std_fit = np.delete(std_fit,faulty_pairs_index)

if show_graph == 'yes':
    plt.figure(1,figsize = (16,8))
    plt.title('Average Temperature Deviation vs. Line Pair (Data compiled with ' + str(nof) + ' stars)')
    plt.scatter(np.arange(0,nop,1),desvios_medios,c = std_desvios_medios)
    plt.grid()
    plt.ylabel('Average Temperature Deviation')
    plt.xlabel('Pair Index')
    plt.colorbar(label = 'Star Temperature STD')

    #plt.figure(2,figsize = (16,8))
    #plt.title('Average Temperature Deviation vs. Line Pair (Data compiled with ' + str(nof) + ' stars)')
    #plt.scatter(np.arange(0,nop,1),desvios_medios,c = std_fit)
    #plt.grid()
    #plt.ylabel('Average Temperature Deviation')
    #plt.xlabel('Pair Index')
    #plt.colorbar(label = 'Pair Fit Temperature STD')

indexes = np.arange(0,nop,1)
#now we want to chose which line pairs stay

#main removal on fixed interval
remove_pairs_index = np.where(abs(desvios_medios)>valid_fits_interval)[0]
desvios_medios = np.delete(desvios_medios,remove_pairs_index)
std_desvios_medios = np.delete(std_desvios_medios,remove_pairs_index)
indexes = np.delete(indexes,remove_pairs_index)
#print(len(indexes))

#second removal, check which of the points does not go outside of the main upper or lower bound when considering STD
remove_pairs_index = np.where(std_desvios_medios>max_std_value)[0]
desvios_medios = np.delete(desvios_medios,remove_pairs_index)
std_desvios_medios = np.delete(std_desvios_medios,remove_pairs_index)
indexes = np.delete(indexes,remove_pairs_index)
#print(len(indexes))

print(len(indexes))

#now we need to make a new complete ratio_list on the correct dir so we can rerun TMCalc with the new restrictions

split_name = data_dir.split('_')
split_name_len = len(split_name)
if split_name_len == 3:
    save_path = 'Graphs_' + str(split_name[1]) + '_' + str(split_name[2]) + '/Graphs/'
elif split_name_len == 4:
    save_path = 'Graphs_' + str(split_name[1]) + '_' + str(split_name[2]) + '/Graphs_'  + str(split_name[3])
elif split_name_len == 5:
    save_path = 'Graphs_' + str(split_name[1]) + '_' + str(split_name[2]) +'/Graphs_' + str(split_name[3]) + '_' + str(split_name[4])
print(save_path)
np.savetxt(save_path + 'indexes',indexes)#saves de used indexes

file = open(save_path+'ratios_list','r')
file_lines = file.readlines()
file.close()

new_file = open(save_path + 'ratios_list_v2','w')
new_file.write(file_lines[0])

for i in range(len(file_lines)-1):
    if len(np.where(indexes==i)[0]) != 0:
        new_file.write(file_lines[i+1])
new_file.close()

plt.figure(2,figsize = (16,8))
plt.title('Average Temperature Deviation vs. Line Pair (Data compiled with ' + str(nof) + ' stars)')
plt.scatter(indexes,desvios_medios,c = std_desvios_medios)
plt.grid()
plt.ylabel('Average Temperature Deviation')
plt.xlabel('Pair Index')
plt.colorbar(label = 'Star Temperature STD')
plt.show()
