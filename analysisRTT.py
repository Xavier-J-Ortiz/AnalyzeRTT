'''
Parse S3 logs downloaded on the local file system. Then do some math
and analyze results.
Currently a moving target by Xavier-J-Ortiz
Debating whether to later load logs directly from S3 bucket, but first want to
correctly load, parse, and analysis data down.
'''
import gzip, os
import simplejson as json

# functions

def unpack_files():
    '''
    unpack_files - grabs a file_path, looks at all files ending in .gz
    opens them up, prints out content, saves in test.txt.
    '''
    file_path = "/home/xortiz/cedexis/S3LogsTest/01"
    actual_content = ""

    for root, dirs, files in os.walk(file_path):

        ### added these lines below just to see what was being housed in root/dirs/files
        ### and see what was going on. Might take this out in a later version
        # print "This is the root: " + root
        # print "This is the dirs : " + str(dirs)
        # print "This is the files : " + str(files)
        ###

        for file in files:
            unzipped_file = ""
            if file.endswith(".gz"):
                full_file_path = root + "/" + file
                unzipped_file = gzip.open(full_file_path, 'rb')
                actual_content += unzipped_file.read()
    return actual_content.split('\n')


def json_create_python_dict(json_concatenated_object):
    '''
    :param json_concatenated_object: output of unpack_files()
    :return: returns a timestamp sorted list of dictionaries from the resulting json input logs
    '''

    parsed_list = []

    print 'tock'

    for json_object in json_concatenated_object:
        if (json_object != ""):
            python_object = json.loads(json_object)
            parsed_list.append(python_object)
    #sorted function done during the return.
    print 'schlock'
    return sorted(parsed_list, key=lambda k: k['timestamp'])

def create_x_axis(dict_translation):
    '''
    will output a list of x axis points that can be nicely read on a graph
    :param dict_translation: output of json_create_python_dict, in other words
    a python dictionary translation of a JSON object
    :return: a list containing only 'X' axis values parsed accordingly to be plopped into pyplot
    '''

    x_axis_list = []
    print 'bloc'
    for entry in dict_translation:
        x_axis_list.append(entry['timestamp'])

    return x_axis_list

def x_segment_by_hour(x_timestamp):
    '''
    will return a list of lists of timestamps in 1 hour chunks, which can be mapped to the
    python dictionary and help with averaging the fastly and akamai RTT data
    :param x_timestamp: dictionary of sorted time stamps to be evaluated. This input represents the data collected in a day

    :return:
    '''

    #create the possible hours in the day to parse in strings
    possible_hours = []
    for hour in range(0, 24):
        if (hour < 10):
            possible_hours.append('0' + str(hour))
        else:
            possible_hours.append(str(hour))

    #print possible_hours

    segmented_timestamps = []
    answer = {}
    # create empty dict
    for hour in possible_hours:
        answer[hour] = []
    print 'tick'
    for entry in x_timestamp:
        current_hour = str(entry).split('T')[1].split(':')[0]
        # print current_hour
        for hour in possible_hours:
            if current_hour == hour:
                answer[hour].append(entry)

    return answer



### save actual_content to test.txt
### useful to verify unpack_files with a finetooth comb
### aka: favorite text editor
# new_test_file = open('test.txt', 'w')
# new_test_file.write(unpack_files())
# new_test_file.close()
###

### quick sanity test of json_create_python_dict
# test_answer = json_create_python_dict(unpack_files())
# print str(test_answer[0]['reason_code']) + "\n"
# print str(test_answer[1]['ttl']) + "\n"

### sanity test for timestamp order is correct for json_create_python_dict
# test_answer = json_create_python_dict(unpack_files())
# new_test_file = open('test_timestamp_order.txt', 'w')
# for json_test_object in test_answer:
#     new_test_file.write(json_test_object['timestamp'] + "\n")
# new_test_file.close()

### sanity test for create_x_axis output

# test_x_axis = create_x_axis(json_create_python_dict(unpack_files()))

###sanity test for parsing out x axis hourly data.

hourly_x_axis_dict = x_segment_by_hour(create_x_axis(json_create_python_dict(unpack_files())))

print hourly_x_axis_dict['00'][0]
print hourly_x_axis_dict['22'][0]
print hourly_x_axis_dict['03']