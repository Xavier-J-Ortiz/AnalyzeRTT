import plot_pickle
file_path = "/home/xortiz/cedexis/S3LogsTest/01"
pickle_name = "pickled_data.pckl"

plot_pickle.plot_a_vs_f(plot_pickle.check_and_create_data(file_path, pickle_name), 10)
