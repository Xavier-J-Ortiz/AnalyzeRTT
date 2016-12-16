'''
Parse S3 logs downloaded on the local file system. Then do some math
and analyze results.
Currently a moving target by Xavier-J-Ortiz
Debating whether to later load logs directly from S3 bucket, but first want to
correctly load, parse, and analysis data found locally.
'''
import gzip, os
# import time

# functions

# tick tock and shlock are commented out and can be uncommented/printed in order to see if / where
# code is stuck due to my oversight, or just taking forever to churn.

def unpack_files(filepath_to_walk):
    '''
    unpack_files - grabs a file_path, looks at all files ending in .gz
    opens them up, prints out content, saves in test.txt.
    :param filepath_to_walk: root path that it will traverse to find .gz files from S3 openmix logs.
    :return: list of extracted json objects. one per list #.
    '''
    actual_content = ""

    for root, dirs, files in os.walk(filepath_to_walk):

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
    # print 'tick'
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

def create_data_points(json_concatenated_object):
    '''
    extract fastly and akamai data points, sorted by timestamp.
    :param json_concatenated_object: output of unpack_files()
    :return: returns a timestamp sorted list of lists from the resulting json input logs, i.e: [[timestamp, akamai_rtt, fastly_rtt]]
    '''

    parsed_list = []

    # print 'tock'

    for json_object in json_concatenated_object:
        if (json_object != ""):
            timestamp = my_splitter(json_object, '"timestamp":"', '"')
            context = my_splitter(json_object, '"context":', ',"used_edns"')
            if (context != '{"none":true}'):
                unparsed_akamai = my_splitter(context, '"akamai_ssl":', ',"fastly_ssl":')
                akamai_rtt = my_splitter(unparsed_akamai, '"http_rtt":', '}')

                unparsed_fastly = my_splitter(context, ',"fastly_ssl":', '}}') + '}'
                fastly_rtt = my_splitter(unparsed_fastly, '"http_rtt":', '}')

                list = [timestamp, akamai_rtt, fastly_rtt]
            # list = [timestamp, context]
            parsed_list.append(list)
    # print 'schlock'
    # decided to sort on return. Done below
    return sorted(parsed_list, key = lambda x : x[0])
