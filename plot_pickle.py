'''
This file has some functions that will allow plotting of information, starting with assurig that parsing and
pickling functions in analysisRTT have been run, as well as check to see if files exist locally, and ask if overwrite.
Plotting functions should load data from pickled file, as this will save time from reloading and parsing the
information from scratch on each plot.
'''
import analysisRTT, os, datetime, time
import matplotlib.pyplot as plt

def check_and_create_data(filepath, pickle_name):
    '''
    Checks if a pickle file exists that it can load to return a datapoint list. If no file exists, then it asks if you
    want to create one, and will return a datapoint list after creation.
    :param filepath: absolute path to traverse in order to gather data from .gz files downloaded from the S3 bucket
    :param pickle_name: name of the pickle file to create or load (string)
    :return: returns list of the following data points: [timestamp, akamai_RTT, fastly_RTT]. Will create a Null value if
    an existing pickle file is not loaded (no output).
    '''
    # if no pickle file with specified name exists, create.
    if (os.path.isfile(pickle_name) == False):
        print "First time " + pickle_name + " is being created on disk.\n"
        return analysisRTT.time_to_gather_and_pickle_data(filepath, pickle_name)
    # if a pickle file exists, prompt user if overwrite is OK.
    else:
        overwrite_prompt = raw_input("\n" + pickle_name + " exists on disk. Would you like to overwrite? (y/n): ")
        # if overwrite OK, overwrite the file and return a datapoint list.
        if (overwrite_prompt == "y" or overwrite_prompt == "Y"):
            print "you have selected 'y' and " + pickle_name + " will be overwritten.\n"
            return analysisRTT.time_to_gather_and_pickle_data(filepath, pickle_name)
        # if overwrite not OK
        elif (overwrite_prompt == "n" or overwrite_prompt == "N"):
            print "You have selected 'n'. the file " + pickle_name + "is not overwritten" +\
                  "\nPlease use another file name or rename " + pickle_name + " to another file name\n" + \
                  "in order to avoid overwriting."
            # ask if existing pickle file should be loaded
            load_prompt = raw_input("\nwould you like to load the data in the existing " + pickle_name + " file? (y/n): ")
            # if pickle file should be loaded, return pickled datapoint list.
            if (load_prompt == "y" or load_prompt == "Y"):
                print "loading the file " + pickle_name + ". It's data shall be returned."
                return analysisRTT.open_and_consume_pickled_data(pickle_name)
            # if pickle is not to be loaded, don't load, return 'None'
            elif (load_prompt == "n" or load_prompt == "N"):
                print "File will not be loaded. None will be returned. Have a nice day!"
                return None
            # if incorrect input on prompt, error
            else:
                raise ValueError("wrong prompted value.\nPlease re-run and input a valid answer when prompted " +
                             "with a 'y' or a 'n'.")
        # if incorrect input on prompt, error
        else:
            raise ValueError("wrong prompted value.\nPlease re-run and input a valid answer when prompted " +
                             "with a 'y' or a 'n'.")

def plot_akamai_vs_fastly(data_points, time_interval):
    '''
    Takes the properly formatted datapoints list, and creates a visualization of akamaiRTT and fastlyRTT
    :param data_points: properly formatted list of datapoints where each datapoint is [timestamp, akamaiRTT, fastlyRTT]
    :param time_interval: interval of time to aggregate the difference
    :return: Doesn't return anything, just displays the graph.
    '''
    x = []
    y = []
    # sets the very first time stamp as the current
    current_timestamp = data_points[0][0]
    # sets the next time stamp as the current plus a time delta of value time_interval
    next_timestamp = current_timestamp + datetime.timedelta(minutes = time_interval)

    y_cumulative = 0
    counter = 0
    start_time = time.time()
    # cycle through the sorted datapoint object.
    for datapoint in data_points:
        # if curr timestamp is larger than last timestamp in dataset
        if (datapoint[0] < next_timestamp):
            # line below represents --> y = akamai_rtt - fastly_rtt
            y_cumulative += (datapoint[1] - datapoint[2])
            counter += 1

        else:
            avrg_time_chunk_of_y = y_cumulative / counter
            y.append(avrg_time_chunk_of_y)
            x.append(current_timestamp)

            current_timestamp = current_timestamp + datetime.timedelta(minutes = time_interval)
            next_timestamp = current_timestamp + datetime.timedelta(minutes = time_interval)
            y_cumulative = 0
            counter = 0
    # for large data sets, it is likely that the last data point available won't be triggering the else. It is more
    # likely that it will have a non zero y_cumulative counter. So, to gather this (possibly) partial datapoint,
    # we have to create and append the last data point to the lists x and y.
    avrg_time_chunk_of_y = y_cumulative / counter
    y.append(avrg_time_chunk_of_y)
    x.append(current_timestamp)
    # time information for running the difference data points.
    print "load time for diff datapoints: " + str(time.time() - start_time)

    # plot information
    plt.plot(x, y, 'rx')
    plt.xlabel('Time - datapoints every ' + str(time_interval) + ' minutes')
    plt.ylabel("millisecond difference between akamai's RTT and fastly's RTT\npositive values mean fastly RTT is better\nnegative values mean akamai RTT is better")
    plt.title("Comparison of fastly's RTT and akamai's RTT averaged over a " + str(time_interval) + " minute interval")
    plt.grid(linestyle = "--")
    plt.show()
