import os
import pandas as pd
from datetime import datetime, timedelta

def get_grouped_files(csv_files, time):
    """
    Returns a list of file paths that were created within 24 hours of the given time.
    """
    time_24_hours_ago = time - timedelta(hours=24)
    grouped_files = []
    for file in csv_files:
        file_time = datetime.fromtimestamp(os.path.getctime(file))
        if time_24_hours_ago <= file_time <= time:
            grouped_files.append(file)
    return grouped_files

# Specify the path to the folder containing the CSV files
folder_path = "C:/Users/lohit/OneDrive/Desktop/SJC/BSNL/MSOFTX_20230101/All"

# Specify the path to the parent folder where the merged files should be saved
parent_folder = "C:/Users/lohit/OneDrive/Desktop/SJC/BSNL/MSOFTX_20230101/Merged"

# Get a list of all CSV files in the folder
csv_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv')]

# Segregate the files based on their creation time
files_by_time = {}
for file in csv_files:
    file_time = datetime.fromtimestamp(os.path.getctime(file))
    if file_time not in files_by_time:
        files_by_time[file_time] = [file]
    else:
        files_by_time[file_time].append(file)

# Merge the files created within 24 hours of each other
for time, group in files_by_time.items():
    grouped_files = get_grouped_files(group, time)
    if len(grouped_files) > 1:
        merged_csv = pd.concat([pd.read_csv(file) for file in grouped_files])
        merged_csv.to_csv(parent_folder + '/' + "merged_" + str(time) + ".csv", index=False)
