import gzip

def unpackFiles():

    unzippedFile = gzip.open('/home/xortiz/cedexis/S3LogsTest/12/1-14290-openmix-json-2016-12-12T12-33-00Z-m1-w9-c0.gz', 'rb')
    actualContent = unzippedFile.read()
    print actualContent

unpackFiles()
