import os
import pandas as pd

# specify the directory you want to use
directory = '.\data'

merged_data = pd.DataFrame()
dataframes = []

for filename in os.listdir(directory):
    if filename.endswith("_csv"):
        # replace . with _ in the filename
        new_filename = filename.replace('.', '_')
        new_filename=new_filename.replace('_csv', '.csv')
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
        
        # read the csv file
        data = pd.read_csv(os.path.join(directory, new_filename))
        
       # append the dataframe to the list
        dataframes.append(data)

# concatenate all the dataframes in the list
merged_data = pd.concat(dataframes, ignore_index=True)

# save the merged data to a single csv file

merged_data.to_csv(os.path.join(directory, 'merged.csv'), index=False)
