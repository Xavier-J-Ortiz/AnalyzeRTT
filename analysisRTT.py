'''
Parse S3 logs downloaded on the local file system. Then do some math
and analyze results.
Currently a moving target by Xavier-J-Ortiz
Debating whether to later load logs directly from S3 bucket, but first want to
correctly load, parse, and analysis data found locally.
'''
import gzip, os
import cPickle as pickle
import time
import datetime

def unpack_files(filepath_to_walk):
    '''
    unpack_files - grabs a file_path, looks at all files ending in .gz
    opens them up, prints out content, saves in test.txt.
    :param filepath_to_walk: root path that it will traverse to find .gz files from S3 openmix logs.
    :return: list of extracted json objects. one per list #.
    '''
    actual_content = ""
    # walk the down the filepath, open and save .gz data, return split data
    for root, dirs, files in os.walk(filepath_to_walk):
        for file in files:
            if file.endswith(".gz"):
                full_file_path = root + "/" + file
                unzipped_file = gzip.open(full_file_path, 'rb')
                actual_content += unzipped_file.read()
    # returns a list with each JSON entry as the element
    return actual_content.split('\n')

def my_splitter(sentence, head, tail):
    '''
    splits strings with a distinct beginning and end.
    :param sentence: string to split
    :param head: beginning of string to split
    :param tail: end of string to split
    :return:
    '''

    end_of_head = sentence.index(head) + len(head)
    start_of_tail = sentence.index(tail, end_of_head)
    return sentence[end_of_head:start_of_tail]

def timestamp_splitter(json_object):
    '''
    Created a helper app that splits and returns a datetime object without using datetime.strptime. Strptime although
    useful is very resource intensive.
    :param json_object: json string.
    :return: datetime.datetime object.
    '''
    # raw_timestamp looks something like this 2016-12-12T03:24:03Z
    raw_timestamp = my_splitter(json_object, '"timestamp":"', '"')
    # datetime.datetime object
    parsed_timestamp = datetime.datetime(int(raw_timestamp[0:4]), int(raw_timestamp[5:7]), int(raw_timestamp[8:10]),
                                         int(raw_timestamp[11:13]), int(raw_timestamp[14:16]),
                                         int(raw_timestamp[17:19]))
    return parsed_timestamp


def create_data_points(json_concatenated_object):
    '''
    extract fastly and akamai data points, sorted by timestamp.
    :param json_concatenated_object: output of unpack_files()
    :return: returns a timestamp sorted list of lists from the resulting json input logs, i.e: [[timestamp, akamai_rtt, fastly_rtt]]
    '''
    parsed_list = []
    for json_object in json_concatenated_object:
        # there were blank json entries. So.... If not blank, parse.
        if (json_object != ""):
            # timestamp is a datetime object that is created from a string containing a timestamp from the JSON.
            # datetime object is very useful in the creation of the actual final data prior to plot as the object
            # allows easy time comparison, addition, and presentation in pyplot (for plotting)
            timestamp = timestamp_splitter(json_object)
            context = my_splitter(json_object, '"context":', ',"used_edns"')
            # there were context entries that did not have detailed information about the CDNs. So...
            # if there is detailed information in the context (aka: NOT '{"none":true}'), parse.
            if (context != '{"none":true}'):
                # opted to not use one-liners for readability.
                # akamai_rtt
                unparsed_akamai = my_splitter(context, '"akamai_ssl":', ',"fastly_ssl":')
                akamai_rtt = int(my_splitter(unparsed_akamai, '"http_rtt":', '}'))
                # fastly_rtt
                unparsed_fastly = my_splitter(context, ',"fastly_ssl":', '}}') + '}'
                fastly_rtt = int(my_splitter(unparsed_fastly, '"http_rtt":', '}'))
                # actual datapoint with RTT taken at that particular moment in time.
                list = [timestamp, akamai_rtt, fastly_rtt]
            # List of all the timestamped datapoints.
            parsed_list.append(list)
    # returned a sorted list of the datapoints from events that happened first, to the events that happened last
    return sorted(parsed_list, key = lambda x : x[0])

def time_to_gather_and_pickle_data(the_file_path, pickle_name):
    '''
    creates data from the .gz files from the pointed the_file_path and pickles the data
    :param the_file_path: path where the data to be harvested is located (string)
    :param pickle_name: name to pickle file to (string)
    :return: returns data points that were pickled.
    '''
    # unpack .gz file, record, and create the initial JSON-decoded data structure
    print "Some useful info: "
    start_time = time.time()
    answer = create_data_points(unpack_files(the_file_path))
    print "\ntime to execute data point creation: " + str(time.time() - start_time)
    print "length of output: " + str(len(answer))
    print "first item output: " + str(answer[0][0]) + "\nlast item timestamp: " + str(answer[-1][0]) + "\n"
    # create pickle file for later consumption. That is, no need to harvest and parse large dataset.
    start_time = time.time()
    pickle.dump(answer, open(pickle_name, 'wb'))
    print "\ntime to execute creation of " + pickle_name + ": " + str(time.time() - start_time)
    # good idea to create pickled data, and also return the answer.
    return answer

def open_and_consume_pickled_data(pickle_name):
    '''
    creates the original object that was pickled. in this case, just the list containing important JSON information.
    :param pickle_name: name of the pickle file.
    :return: list with data points ready for analysis [timestamp, akamai_rtt, fastly_rtt]
    '''
    # pretty straight forward. Load a pickled file with some useful time performance data tagged.
    start_time_unpickle = time.time()
    answer = pickle.load(open(pickle_name, 'rb'))
    print "load time to unpickle and have data ready: " + str(time.time() - start_time_unpickle)
    return answer
