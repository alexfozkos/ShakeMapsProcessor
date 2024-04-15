import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# Define the directory containing all the folders
main_folder = 'Data/SCARDEC/'
# Define Magnitude threshold for selection
threshold = 7.0
# Initialize peak time array
peak_tn = np.array([])
# Loop through each folder in the main folder
for folder in os.listdir(main_folder):
    folder_path = os.path.join(main_folder, folder)

    # Check if the item in the main folder is a directory
    if os.path.isdir(folder_path):
        # Assuming your time series data is stored in a text file within each folder
        for file in os.listdir(folder_path):
            if file.startswith('fctoptsource'):  # Assuming your data files have a .txt extension
                file_path = os.path.join(folder_path, file)

                # Read the first two lines of the text file
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                    # Extract the relevant information from the second line
                    second_line_info = lines[1].split(' ')
                    mw = float(second_line_info[2])
                    # Check if the data should be processed based on the extracted information
                    if mw >= threshold:  # Assuming you have a threshold value
                        # Read the rest of the text file into a pandas DataFrame
                        df = pd.read_csv(file_path, skiprows=2, delim_whitespace=True, names=['time', 'moment_rate'])
                        # Get duration from max time while moment rate is >0
                        duration = df.loc[df['moment_rate'] > 0]['time'].max()
                        # Normalize time data to the duration
                        tn = df['time'].copy()/duration
                        # Grab the normed time at peak moment rate and save into array
                        peak_tn = np.append(peak_tn, tn.loc[df['moment_rate'].idxmax()])

data = peak_tn
q5, q10, q25, q50, q75, q90, q95 = np.percentile(data, [5, 10, 25, 50, 75, 90, 95])
iqr = q75-q25
left_whisker = q25 - 1.5*iqr
right_whisker = q75 + 1.5*iqr
counts, bins = np.histogram(data, bins=20)
print(bins)
plt.figure()
plt.stairs(counts, bins)
plt.axvline(q25, ls='--', c='k', lw=1)
plt.axvline(q75, ls='--', c='k', lw=1)
plt.axvline(q10, ls=':', c='r', lw=1)
plt.axvline(q90, ls=':', c='r', lw=1)
plt.axvline(q5, ls=':', c='b', lw=1)
plt.axvline(q95, ls=':', c='b', lw=1)
plt.axvline(left_whisker, ls='-', c='k', lw=1)
plt.axvline(right_whisker, ls='-', c='k', lw=1)
plt.axvline(data.mean(), lw=1.5, c='purple')
plt.axvline(np.median(data), lw=1.5, c='k')
plt.title('Histogram')
plt.ylabel('Counts')
plt.xlabel('Normalized Centroid Timeshift')
print(q5, q10, q25, q50, q75, q90, q95)