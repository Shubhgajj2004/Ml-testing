import os
import pandas as pd

def file_renames(filename: str):
    df = pd.read_csv(filename)
    start = df.iloc[0]['index']
    end = df.iloc[-1]['index']
    new_file_name = f'Test_out/test_out-{start}-{end}.csv'
    df.to_csv(new_file_name, index=False)
    os.remove(filename)

file_name = 'Test_out/test_out (1).csv'
file_renames(file_name)