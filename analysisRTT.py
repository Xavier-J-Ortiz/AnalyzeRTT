'''
Parse S3 logs loaded on the local file system. Do some math.
Analyze results.
Currently a moving target by Xavier-J-Ortiz
'''
import gzip, os

# functions

def unpack_files():
    '''
    unpack_files - grabs a file_path, looks at all files ending in .gz
    opens them up, prints out content.
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

unpack_files()