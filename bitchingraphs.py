# import libraries
import csv 
import matplotlib.pyplot as plt

# !!!!!!!!!!!!!!
# instructions on how to add other data types
# add a setting include_[data type] = True in the settings section below
# under read logic, add a new if statement for the data type following the same format. make sure you get the correct column header
# do this for both dataset1 and dataset 2
# everything else should be automatic because I'm a fucking gangsta
# !!!!!!!!!!!!!!

# settings
strip_end = True # Set to True if the dataset includes extra data at the column end (otherwise process will crash)
trim_start = False # Set to True if you want to localize the datasets to the end of the data
include_number_at_end = 200 # number of data points to include at the end of the dataset if trim_start = True

# include data, set to False if not going looking at any particular data
include_gpu_rail_voltages = False
include_frame_time = False
include_cpu_power_package_wattage = False
include_gpu_temperature = False
include_gpu_memory_allocated = True
include_d3d_allocated = False

# percentage toggle
look_at_percentage = True

# compare_toggle
compare_toggle = True

# dataset 1
# change to filename of dataset
# either this file needs to be in the same directory of the datasets, or you need to provide the full path below
dataset1 = '2.CSV' 
dataset2 = '11.CSV' # only used if compare_toggle = True

# read in logic
# dataset 1
with open(dataset1, mode='r') as file:
    csv_reader = csv.DictReader(file)
    dataset1array = []
    if include_gpu_rail_voltages:
        dataset1array.append([row['GPU Rail Voltages (avg) [V]'] for row in csv_reader])
    if include_frame_time:
        dataset1array.append([row['Frame Time [ms]'] for row in csv_reader])
    if include_cpu_power_package_wattage:     
        dataset1array.append([row['CPU Package Power [W]'] for row in csv_reader])
    if include_gpu_temperature:
        dataset1array.append([row['GPU Temperature [°C]'] for row in csv_reader])
    if include_gpu_memory_allocated:
        dataset1array.append([row['GPU Memory Allocated [MB]'] for row in csv_reader])
    if include_d3d_allocated:
        dataset1array.append([row['GPU D3D Memory Dedicated [MB]'] for row in csv_reader])

# dataset 2
if compare_toggle:
    with open(dataset2, mode='r') as file:
        csv_reader = csv.DictReader(file)
        dataset2array = []
        if include_gpu_rail_voltages:
            dataset2array.append([row['GPU Rail Voltages (avg) [V]'] for row in csv_reader])
        if include_frame_time:
            dataset2array.append([row['Frame Time [ms]'] for row in csv_reader])
        if include_cpu_power_package_wattage:     
            dataset2array.append([row['CPU Package Power [W]'] for row in csv_reader])
        if include_gpu_temperature:
            dataset2array.append([row['GPU Temperature [°C]'] for row in csv_reader])
        if include_gpu_memory_allocated:
            dataset2array.append([row['GPU Memory Allocated [MB]'] for row in csv_reader])
        if include_d3d_allocated:
            dataset2array.append([row['GPU D3D Memory Dedicated [MB]'] for row in csv_reader])

# strip end logic
if strip_end:
    dataset1array = [x[:len(x)-2] for x in dataset1array]
    if compare_toggle:
        dataset2array = [x[:len(x)-2] for x in dataset2array]

# percentage logic
if look_at_percentage:
    dataset1array = [[float(x) / max(map(float, dataset)) * 100 for x in dataset] for dataset in dataset1array]
    if compare_toggle:
        dataset2array = [[float(x) / max(map(float, dataset)) * 100 for x in dataset] for dataset in dataset2array]

# time logic
# note that to correctly plot, we need to assure that all arrays have the same length, so we trim the length of the longer array to the length of the shortest array
# data is removed FROM THE FRONT OF THE LONGER LIST
if trim_start:
    dataset1array = [x[len(x)-include_number_at_end:] for x in dataset1array]
    if compare_toggle:
        dataset2array = [x[len(x)-include_number_at_end:] for x in dataset2array]
if compare_toggle:
    time = list(range(0, 2*len(max(dataset1array[0], dataset2array[0])), 2))
    if len(dataset1array[0]) > len(dataset2array[0]):
        dataset1array = [x[len(dataset1array[0])-len(dataset2array[0]):] for x in dataset1array]
    else:
        dataset2array = [x[len(dataset2array[0])-len(dataset1array[0]):] for x in dataset2array]
else:
    time = list(range(0, 2*len(dataset1array[0]), 2))

# plot logic 
for data in dataset1array:
    plt.plot(time, data, label='Dataset 1')
if compare_toggle:
    for data in dataset2array:
        plt.plot(time, data, label='Dataset 2')    

plt.xlabel('Time (S)')
if look_at_percentage:
    plt.ylabel('Percentage data')
else:
    plt.ylabel('Absolute data')
plt.legend()
plt.show()
