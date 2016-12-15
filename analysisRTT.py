'''
Parse S3 logs downloaded on the local file system. Then do some math
and analyze results.
Currently a moving target by Xavier-J-Ortiz
Debating whether to later load logs directly from S3 bucket, but first want to
correctly load, parse, and analysis data down.
'''
import gzip, os

# functions

def unpack_files():
    '''
    unpack_files - grabs a file_path, looks at all files ending in .gz
    opens them up, prints out content, saves in test.txt.
    '''
    file_path = "/home/xortiz/cedexis/S3LogsTest/12"
    actual_content = ""

    for file in os.listdir(file_path):

        unzipped_file = ""

        if file.endswith(".gz"):
            full_file_path = file_path + "/" + file
            unzipped_file = gzip.open(full_file_path, 'rb')
            actual_content += unzipped_file.read()

    print actual_content

    new_test_file = open('test.txt', 'w')
    new_test_file.write(actual_content)
    new_test_file.close()

unpack_files()