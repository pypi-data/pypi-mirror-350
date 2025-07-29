import pandas as pd
import glob
import os
from tqdm import tqdm

def combineCSVFiles(input_path, output_file):  
    all_files = glob.glob(os.path.join(input_path, "*.csv"))  
    print(f"Found {len(all_files)} CSV files in the directory: {input_path}")
    print(f"Output file will be saved as: {output_file}")
    if not input_path or not output_file:
        raise ValueError("Input and output paths must be provided.")
    
    if not os.path.isdir(input_path):
        raise FileNotFoundError(f"The directory {input_path} does not exist.")
    
    input_path = os.path.abspath(input_path)

    
    if not all_files:
        raise FileNotFoundError(f"No CSV files found in the directory: {input_path}")
    
    df_list = [] #list to hold all dataframes

    for file in tqdm(all_files, desc="Processing CSV files"): #tdqm for progress bar, loop through all csv's in input path directory
        df = pd.read_csv(file)
        df_list.append(df)
    
    combined_df = pd.concat(df_list, ignore_index=True) #concatenate all dfs in list
    
    combined_df.to_csv(output_file, index=False) #save to output file
    print(f"Combined CSV saved to: {output_file}") 
    print(f"Total rows in combined file: {len(combined_df)}")

if __name__ == "__main__":
    input_path = input("Enter the path to the directory containing CSV files: ")
    output_file = input("Enter the name of the output CSV file (e.g., combined.csv): ")
    
    try:
        combineCSVFiles(input_path, output_file)
    except Exception as e:
        print(f"An error occurred: {e}")

