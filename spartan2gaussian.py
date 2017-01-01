#
#   USAGE: 
#       python2.6 file1.sdf file2.sdf file3.sdf ...
#       
#
#   By Yuhong Liu (Dec 16th, 2016)
#
import sys
import os

# Get all command line arguments ( file1.sdf ... )
all_inputs = sys.argv[1:]


# Please Make Changes Here to Accommodate Different JobTypes.
memory   = '%mem=15gb'
ncpu     = '%nproc=8'
nosave   = '%nosave' 
jobtype  = '#P opt freq hf/3-21g*'
comments = 'Candidate Structure: initial geometry optimization and frequency calculation with HF'
charge_multi = '0 1'
com_file_suffix = '_HF_opt_conf'


# String Manipulations:
prefix1 =  memory + '\n'   + ncpu    + '\n'   + '%chk='
prefix2 =  nosave + '\n\n' + jobtype + '\n\n' + comments + '\n\n' + charge_multi + '\n'

for item in all_inputs:
	os.system("dos2unix "+item)  # Convert Windows newline to Unix newline
	f = open(item)               # open and read Spartan file
	lines = f.read()
	f.close()
	molecules = lines.split('$$$$')[:-1]  # Last line is empty so discard it...
	for n in range(len(molecules)): 
		mol = molecules[n]
		mol_lines   = mol.split('\n')     # Break up chunk by newlines
		coordinate_lines = [ line.split() for line in mol_lines if '0  0  0  0  0  0  0  0  0  0  0  0' in line ]          # Retrieve Coordinate Lines
		coordinates = [ line[3] +'    '+ line[0] +'    '+ line[1] +'    '+ line[2] + '\n' for line in coordinate_lines ]   # Form Gaussian Input Format
		output_buffer = prefix1 + item.split('.')[0] + com_file_suffix + str(n+1) + '.chk\n' + prefix2                      # Construct Gaussian Prefix
		for line in coordinates:
			output_buffer += line    # Add Coordinate Lines to Gaussian Input File
		output_buffer += '\n\n'      # Trailing newlines
		f = open(item.split('.')[0] + com_file_suffix  + str(n+1) + '.com', 'w')  # Write to disk.
		f.write(output_buffer)
		f.close()
