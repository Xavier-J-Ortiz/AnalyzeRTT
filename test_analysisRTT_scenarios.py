import time, analysisRTT

file_path = "/home/xortiz/cedexis/S3LogsTest/01"

###
#  save actual_content to test.txt
# useful to verify unpack_files with a finetooth comb
# aka: favorite text editor
####
#new_test_file = open('test.txt', 'w')
#new_test_file.write(analysisRTT.unpack_files())
#new_test_file.close()

###
#  test unpack and create data points
# with some timing features and the option to save to an external file as well
#  just for fun
###
start_time = time.time()
answer = analysisRTT.create_data_points(analysisRTT.unpack_files(file_path))
print "time to execute: " + str(time.time() - start_time)
print answer[500]

#new_test_file = open('test_timestamp_order.txt', 'w')
#new_test_file.write(str(answer))
#new_test_file.close()

print "length of output: " + str(len(answer))
print "first item output: " + str(answer[0][0]) + "\nlast item timestamp: " + str(answer[-1][0])
