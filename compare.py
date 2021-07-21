import numpy as np
import time as t
from functions import *
import progress.bar as pb

initial_t = t.time()

options = get_settings('compare_options')

n = int(options[0])
file_name1 = options[1]
folder = options[2]
file_out = options[3]


noe = 0 # number of exceptions

#set file paths
file_path2 = folder + 'Parameters/'


#need to create to identical structures that enables comparinson

file1 = open(file_name1, 'r')
file1_data = np.asarray(file1.readlines())
file1.close()

nol = len(file1_data) #nol = number of lines
data1 = np.zeros([nol-1,3],dtype = float)
pos1 = np.array([2,4,5])#sets the position of the data we want to retrieve, sdtdev, line1, line2

#set progress bar for comparing and for generating complete line list

bar1 = pb.IncrementalBar('Comparison Progress', max = nol, suffix = '%(index)d/%(max)d')
bar2 = pb.IncrementalBar('Compiling Raio List', max = n, suffix = '%(index)d/%(max)d')

for i in range(1,nol):
	line = np.asarray(file1_data[i].split())
	for j in range(3):
		data1[i-1,j] = float(line[pos1[j]])

output_file = open(folder + file_out + '_compare', 'w')
output_file_re = open(folder + file_out + '_re', 'w')
output_file.write(file1_data[0].replace('\n','') + '  Δstddev  present?  stddevlevel\n')
output_file_re.write('pair'.rjust(5) + 'stddev'.rjust(9) + 'line1'.rjust(10) + 'line2'.rjust(10) + 'C0'.rjust(15) + 'C1'.rjust(15) + 'C2'.rjust(15) + 'C3'.rjust(15) + 'flag'.rjust(7) + 'stdlevel'.rjust(11) + '\n')

flag_array = np.zeros(nol-1,dtype = int)
#matched_pairs = np.zeros(0,dtype = int)

for i in range(nol-1):
	line_data1 = data1[i]

	for j in range(n):
		try:
			line_data = get_data(file_path2 + str(j))
		except FileNotFoundError:
			noe += 1
			continue

		std = line_data[0]
		line1 = line_data[1]
		line2 = line_data[2]
		c0 = line_data[3]
		c1 = line_data[4]
		c2 = line_data[5]
		c3 = line_data[6]
		flag_1 = line_data[7]

		if (line1 == line_data1[1] and line2 == line_data1[2]) or (line2 == line_data1[1] and line1 == line_data1[2]):
			#matched_pairs = np.append(matched_pairs,j)
			delta_std = int(line_data[0] - line_data1[0]) # negative is better
			flag = 1
			if line_data[0] <= 200:
				level = 'opt'
			elif line_data[0]>200 and line_data[0]<=320:
				level = 'low'
			else:
				level = 'm/h'
			output_file.write(file1_data[i+1].replace('\n','') + '  ' + str(delta_std).rjust(6) + str(flag).rjust(4) + level.rjust(7) + '\n')
			write_line =  str(j).rjust(5) + str(std).rjust(9) + str(line1).rjust(10) + str(line2).rjust(10) + str(c0).rjust(15) + str(c1).rjust(15) + str(c2).rjust(15) + str(c3).rjust(15) + str(flag_1).rjust(7) + level.rjust(11) + '\n'
			output_file_re.write(write_line)
			flag_array[i] = 1
			break
		elif j == n:
			delta_std = '---'
			flag = 0
			optimal = '---'
			output_file.write(file1_data[i+1].replace('\n','') + str(delta_std).rjust(6) + str(flag).rjust(4) + level.rjust(7) + '\n')
	bar1.next()

bar1.finish()
print('\n')

output_file.close()
output_file_re.close()
percentage_of_matches = round(np.sum(flag_array)/len(flag_array),2)*100



output_file = open(folder + file_out, 'w')
output_file.write('pair'.rjust(5) + 'stddev'.rjust(9) + 'line1'.rjust(10) + 'line2'.rjust(10) + 'C0'.rjust(15) + 'C1'.rjust(15) + 'C2'.rjust(15) + 'C3'.rjust(15) + 'flag'.rjust(7) + 'stdlevel'.rjust(11) + '\n')

for j in range(n):
	try:
		line_data = get_data(file_path2 + str(j))
	except FileNotFoundError:
		bar2.next()
		continue

	std = line_data[0]
	line1 = line_data[1]
	line2 = line_data[2]
	c0 = line_data[3]
	c1 = line_data[4]
	c2 = line_data[5]
	c3 = line_data[6]
	flag = line_data[7]

	if std<=320:
		if std <= 200:
			level = 'opt'
		else:
			level = 'low'

		write_line =  str(j).rjust(5) + str(std).rjust(9) + str(line1).rjust(10) + str(line2).rjust(10) + str(c0).rjust(15) + str(c1).rjust(15) + str(c2).rjust(15) + str(c3).rjust(15) + str(flag).rjust(7) + level.rjust(11) + '\n'
		output_file.write(write_line)

	bar2.next()

bar2.finish()
output_file.close()

print('The number of "FileNotFoundError" exceptions were ' + str(noe) + '. The program calculated ' + str(percentage_of_matches) + '% correspondance.')
print('The program took ' + str(int(t.time()-initial_t)) + ' seconds.')
