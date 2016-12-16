'''
Parse S3 logs downloaded on the local file system. Then do some math
and analyze results.
Currently a moving target by Xavier-J-Ortiz
Debating whether to later load logs directly from S3 bucket, but first want to
correctly load, parse, and analysis data down.
'''
import gzip, os, json

# functions

def unpack_files():
    '''
    unpack_files - grabs a file_path, looks at all files ending in .gz
    opens them up, prints out content, saves in test.txt.
    '''
    file_path = "/home/xortiz/cedexis/S3LogsTest"
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

    for json_object in json_concatenated_object:
        if (json_object != ""):
            python_object = json.loads(json_object)
            parsed_list.append(python_object)
    #sorted function done during the return.
    return sorted(parsed_list, key=lambda k: k['timestamp'])

def create_x_axis(dict_translation):
    '''
    will output a list of x axis points that can be nicely read on a graph
    :param dict_translation: output of json_create_python_dict, in other words
    a python dictionary translation of a JSON object
    :return: a list containing only 'X' axis values parsed accordingly to be plopped into pyplot
    '''

    x_axis_list = []

    for entry in dict_translation:
        print entry['timestamp']
        x_axis_list.append(entry['timestamp'])

    return x_axis_list


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

#test_x_axis = create_x_axis(json_create_python_dict(unpack_files()))