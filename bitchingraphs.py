# import libraries
# ---------------------
import csv 
import matplotlib.pyplot as plt

# settings
# ---------------------
strip_end = True # Set to True if the dataset includes extra data at the column end (otherwise process will crash)
trim_start = False # Set to True if you want to localize the datasets to the end of the data
include_number_at_end = 200 # number of data points to include at the end of the dataset if trim_start = True

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# set data_header to whatever data you want to analyze
# commented statements are included for ease of use
# only one should be uncommented at a time
# to add extra data types, simply add a new data_header = ...
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# data headers
# ---------------------
#data_header = 'GPU Rail Voltages (avg) [V]'
#data_header = 'Frame Time [ms]'
#data_header = 'CPU Package Power [W]'
#data_header = 'GPU Temperature [°C]'
data_header = 'GPU Memory Allocated [MB]'
#data_header = 'GPU D3D Memory Dedicated [MB]'

# percentage toggle
# ---------------------
look_at_percentage = True

# compare_toggle
# ---------------------
compare_toggle = True

# dataset files 
# change to filename of dataset
# either this file needs to be in the same directory of the datasets, or you need to provide the full path below
# ---------------------
dataset1 = '2.CSV' 
dataset2 = '11.CSV' # only used if compare_toggle = True

# read in logic
# dataset 1
# ---------------------
with open(dataset1, mode='r') as file:
    csv_reader = csv.DictReader(file)
    dataset1array = [row[data_header] for row in csv_reader]

# dataset 2
# ---------------------
if compare_toggle:
    with open(dataset2, mode='r') as file:
        csv_reader = csv.DictReader(file)
        dataset2array = [row[data_header] for row in csv_reader]

# strip end logic
# ---------------------
if strip_end:
    dataset1array = dataset1array[:len(dataset1array)-2]
    if compare_toggle:
        dataset2array = dataset2array[:len(dataset2array)-2]

# percentage logic
# ---------------------
if look_at_percentage:
    dataset1array = [float(x) / max(map(float, dataset1array)) * 100 for x in dataset1array]
    if compare_toggle:
        dataset2array = [float(x) / max(map(float, dataset2array)) * 100 for x in dataset2array]

# time logic
# note that to correctly plot, we need to assure that all arrays have the same length, so we trim the length of the longer array to the length of the shortest array
# data is removed FROM THE FRONT OF THE LONGER LIST
# ---------------------
if trim_start:
    dataset1array = dataset1[len(dataset1array)-include_number_at_end:]
    if compare_toggle:
        dataset2array = dataset2array[len(dataset2array)-include_number_at_end:]
if compare_toggle:
    time = list(range(0, 2*min(len(dataset1array), len(dataset2array)), 2))
    if len(dataset1array) > len(dataset2array):
        dataset1array = dataset1array[len(dataset1array)-len(dataset2array):]
    else:
        dataset2array = dataset2array[len(dataset2array)-len(dataset1array):]
else:
    time = list(range(0, 2*len(dataset1array), 2))

# plot logic 
# ---------------------
plt.plot(time, dataset1array, label='Dataset 1')
if compare_toggle:
    plt.plot(time, dataset2array, label='Dataset 2')

plt.xlabel('Time (S)')
if look_at_percentage:
    plt.ylabel(data_header + ' (%)')
else:
    plt.ylabel(data_header)
plt.legend()
plt.show()
