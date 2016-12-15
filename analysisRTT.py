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

    ### root file path to traverse for S3 .gz logs
    ### the algo will traverse across the root file system
    ### and pick out the .gz logs.

    file_path = "/home/xortiz/cedexis/S3LogsTest"
    actual_content = ""

    for root, dirs, files in os.walk(file_path):
        ### added these lines below just to see what was being housed in root/dirs/files
        ### and see what was going on.
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

### save actual_content to test.txt
### useful to see if output is getting correctly saved
### and if the function is actually working without
### text puking all over the place.
# new_test_file = open('test.txt', 'w')
# new_test_file.write(unpack_files())
# new_test_file.close()
###

def json_create_python_dict(json_concatenated_object):
    parsed_list = []
    for json_object in json_concatenated_object:
        if (json_object != ""):
            python_object = json.loads(json_object)
            parsed_list.append(python_object)

    return sorted(parsed_list, key=lambda k: k['timestamp'])

### quick sanity test
# test_answer = json_create_python_dict(unpack_files())
# print str(test_answer[0]['reason_code']) + "\n"
# print str(test_answer[1]['ttl']) + "\n"

### should do a quick sanity test for timestamp order too
# TBD