import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({'font.size': 20})


test_sample_temp = np.array([6483.0424,6258.5751,6641.1974,5986.2703,6176.5888,6475.5659,6139.883,6288.0723,6005.9531,6368.4044,6183.6994])
test_sample_STD = np.array([145.2389,82.1456,120.0753,90.16,108.5399,118.6634,124.5277,94.9911,77.8571,108.7197,136.3923])
test_sample_sweet_cat_temp = np.array([6290,6260,6500,6054,5969,6330,6235,6224,6070,6199,6347])
test_sample_sweet_cat_STD = np.array([87,24,35, 19,20,30,28,20,15,27,28])
total_STD = test_sample_STD + test_sample_sweet_cat_STD #the eeror bars used are the sum of the SWEET-Cat STD with the fit STD
test_sample_sweet_cat_met = np.array([-0.24,0.18,-5,0.12,0.17,0.29,0.37,])
test_sample_sweet_cat_logg = np.array([4.29,4.47,3.80, 4.53,3.92,4.03,4.37,4.37,4.53,4.18,4.29])
test_sample_sweet_cat_met = np.array([-0.24,0.18,0.19,0.12,0.17,0.29,0.37,0.04,0.16,-0.11,0.38])
nop = len(test_sample_temp)
x = np.arange(1,nop+1,1)

plt.figure(1,figsize = (16,8))
plt.title('Simple TMCalc Teff vs. SWEET-Cat Temperature')
plt.errorbar(test_sample_sweet_cat_temp,test_sample_temp,yerr = total_STD,xerr = None,marker = 'o', fmt = '.',label = 'Data')
plt.grid()
plt.plot(np.linspace(5900,6600,500),np.linspace(5800,6800,500),'--',label = 'Perfect Tendency')
plt.ylabel('Calibrations Temperature (K)')
plt.xlabel('Sweet Cat Temperature (K)')


plt.legend()


plt.figure(2,figsize = (16,8))
plt.title('Teff difference vs. Logg')
plt.errorbar(test_sample_sweet_cat_logg,test_sample_sweet_cat_temp-test_sample_temp,yerr = total_STD,xerr = None,marker = 'o', fmt = '.',label = 'Data')
plt.grid()
plt.ylabel('Delta Teff')
plt.xlabel('Logg')
plt.legend()
plt.show()

plt.figure(3,figsize = (16,8))
plt.title('Teff difference vs. Metallicity')
plt.errorbar(test_sample_sweet_cat_met,test_sample_sweet_cat_temp-test_sample_temp,yerr = total_STD,xerr = None,marker = 'o', fmt = '.',label = 'Data')
plt.grid()
plt.ylabel('Delta Teff')
plt.xlabel('Metallicity')
plt.legend()
plt.show()

STD_delta_T = np.std(test_sample_sweet_cat_temp-test_sample_temp)
average_STD = np.average(total_STD)

print(STD_delta_T)
print(average_STD)
