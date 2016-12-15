import gzip, os

def unpack_files():
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
