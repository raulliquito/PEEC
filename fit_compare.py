import numpy as np
import matplotlib.pyplot as plt
from functions import *

path = "Graphs_70.0_3.0/Graphs/"
file = "ratios_list"

re_file_data = get_LR_data(path+file + '_re')
compare_file_data = get_compare_file_data(path+file+'_compare')

nop = len(re_file_data)

LR = np.linspace(0.1,15,60000)

for i in range(nop):
    re_data = re_file_data[i]
    re_pair = re_data[0]
    re_std = re_data[1]
    re_line1 = re_data[2]
    re_line2 = re_data[3]
    re_coefs = re_data[4:8]
    flag = re_data[8]

    c_data = compare_file_data[i]
    c_std = c_data[0]
    c_line1 = c_data[1]
    c_line2 = c_data[2]
    c_coefs = c_data[3:7]
    c_flag = c_data[7]

    compare_data = compare_file_data[i]

    plt.figure(i,figsize=(16,8))
    plt.title(str(re_pair) + ': ' + str(re_line1) + ' ' + str(re_line2) + '  ' + str(re_std) + '  ' + str(flag))

    #sets up my fit's values in order to make the graph
    if flag == 1:
        y1 = poly3(1/LR,re_coefs[0],re_coefs[1],re_coefs[2],re_coefs[3])
    elif flag ==2:
        y1 = poly3(np.log(LR),re_coefs[0],re_coefs[1],re_coefs[2],re_coefs[3])
    elif flag==0:
        y1 = poly3(LR,re_coefs[0],re_coefs[1],re_coefs[2],re_coefs[3])

    if re_line1 != c_line1:
        x = 1/LR
    elif re_line1 == c_line1:
        x = LR
    else:
        print('Error at ' + str(re_pair) + '\n')

    if c_flag == 1:
        y2 = poly3(x,c_coefs[0],c_coefs[1],c_coefs[2],c_coefs[3])
    elif c_flag == 2:
        y2 = poly1(x,c_coefs[0],c_coefs[1])
    elif c_flag == 3:
        y2 = poly3(1/x,c_coefs[0],c_coefs[1],c_coefs[2],c_coefs[3])
    elif c_flag == 4:
        y2 = poly1(1/x,c_coefs[0],c_coefs[1])
    elif c_flag == 5:
        y2 = poly3(np.log(x),c_coefs[0],c_coefs[1],c_coefs[2],c_coefs[3])
    elif c_flag == 6:
        y2 = poly1(np.log(x),c_coefs[0],c_coefs[1])

    plt.plot(LR,y1,label = 'My Fit')
    plt.plot(LR,y1+re_std,'--k')
    plt.plot(LR,y1-re_std,'--k')
    plt.plot(LR,y2,label = 'Other Fit')

    plt.ylim(4000,8000)
    plt.grid()
    plt.legend()
    plt.show()
