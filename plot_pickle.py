'''
This file has some functions that will allow plotting of information, starting with assurig that parsing and
pickling functions in analysisRTT have been run, as well as check to see if files exist locally, and ask if overwrite.
Plotting functions should load data from pickled file, as this will save time from reloading and parsing the
information from scratch on each plot.
'''
import datetime

import analysisRTT, os
import matplotlib.pyplot as plt
import matplotlib.dates as md
import time

def check_and_create_data(filepath, pickle_name):
    '''
    checks to see if a pickle file exists. If no pickle file exists, analysisRTT.time_to_gather_and_pickle_data will be
    run.
    If a pickle file exists with the same name as the parameter pickle_name, the user will be prompted to overwrite.
    On overwrite, the function will overwrite the old file pickle_name. Old data will be lost.
    If no overwrite is prompted, the file will be left alone.
    If 'y' or 'n' not input, nothing will happen.
    :param filepath: absolute path to traverse in order to gather data from .gz files downloaded from the S3 bucket
    :param pickle_name: name of the pickle file to create (string)
    :return:
    '''
    if (os.path.isfile(pickle_name) == False):
        print "First time " + pickle_name + " is being created on disk.\n"
        return analysisRTT.time_to_gather_and_pickle_data(filepath, pickle_name)
    ### if a pickle file with the same name as pickle_name exists, prompt user if overwrite is OK.
    else:
        overwrite_prompt = raw_input("\n" + pickle_name + " exists on disk. Would you like to overwrite? (y/n): ")
        if (overwrite_prompt == "y" or overwrite_prompt == "Y"):
            print "you have selected 'y' and " + pickle_name + " will be overwritten.\n"
            return analysisRTT.time_to_gather_and_pickle_data(filepath, pickle_name)
        elif (overwrite_prompt == "n" or overwrite_prompt == "N"):
            print "You have selected 'n'. the file " + pickle_name + "is not overwritten" +\
                  "\nPlease use another file name or rename " + pickle_name + " to another file name\n" + \
                  "in order to avoid overwriting."
            return None
        else:
            raise ValueError("wrong prompted value.\nPlease re-run and input a valid answer when prompted " +
                             "with a 'y' or a 'n'.")

# def create_aggregate_data(pickle_name)

### Test to check 'check_and_create_data' is working correctly.
file_path = "/home/xortiz/cedexis/S3LogsTest/01"
pickle_name = "pickled_data_3_hours.pckl"

#check_and_create_data(file_path, pickle_name)

### Test load time of pickled file,
start_time = time.time()
answer = analysisRTT.open_and_consume_pickled_data(pickle_name)
print "load time to unpickle and have data ready: " + str(time.time() - start_time)
print answer[500]

x = []
y = []

# x_value = 0
for datapoint in answer:
    x.append(datapoint[0])
    # y = akamai_rtt - fastly_rtt
    y.append(float(datapoint[1]) - float(datapoint[2]))
    # x_value += 1


print len(x)
print x[500]

plt.plot(x, y, 'ro')
plt.show()

