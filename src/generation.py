import pandas as pd
import os

# List to store DataFrames
dataframes = []

# Loop through file names dataframe_1.csv to dataframe_17.csv
for i in range(1, 18):
    file_name = f"dataframe_{i}.csv"

    # Check if file exists before reading
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
        dataframes.append(df)
    else:
        print(f"Warning: {file_name} not found.")

# Concatenate all DataFrames
if dataframes:
    final_df = pd.concat(dataframes, ignore_index=True)

    # Save final DataFrame to CSV
    final_df.to_csv("final_dataframe.csv", index=False)
    print("Final CSV saved as final_dataframe.csv")
else:
    print("No files found to concatenate.")
