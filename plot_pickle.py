import analysisRTT, os, time
file_path = "/home/xortiz/cedexis/S3LogsTest/01"
pickle_name = "pickled_data.pckl"
if (os.path.isfile(pickle_name) == False):
    analysisRTT.time_to_gather_and_pickle_data(file_path, pickle_name)
else:
    overwrite_prompt = raw_input("\n" + pickle_name + " exists on disk. Would you like to overwrite? (y/n): ")
    if (overwrite_prompt == "y" or overwrite_prompt == "Y"):
        analysisRTT.time_to_gather_and_pickle_data(file_path, pickle_name)
    elif (overwrite_prompt == "n" or overwrite_prompt == "N"):
        print "\nPlease use another file name or rename " + pickle_name + " to another file name\n" + \
               "in order to avoid overwriting."
    else:
        print "\nPlease re-run and input a valid answer when prompted with a 'y' or a 'n'"


start_time = time.time()
answer = analysisRTT.open_and_consume_pickled_data(pickle_name)
print "load time to unpickle and have data ready: " + str(time.time() - start_time)