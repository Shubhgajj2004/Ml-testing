import pandas as pd
import os

older_file = 'Test_out/temp1.csv'
newer_file = 'Test_out/temp2.csv'

older_df = pd.read_csv(older_file)
newer_df = pd.read_csv(newer_file)

assert list(older_df.columns) == list(newer_df.columns), "CSV files have different structures."

last_index_older = older_df.iloc[-1]['index']

new_index_start_with = older_df.shape[0]
newer_rows_to_add = newer_df.iloc[new_index_start_with:]
updated_older_df = pd.concat([older_df, newer_rows_to_add], ignore_index=False)


start = updated_older_df.iloc[0]['index']
end = updated_older_df.iloc[-1]['index']
new_file_name = f'Test_out/test_out-{start}-{end}.csv'
updated_older_df.to_csv(new_file_name, index=False)

os.remove(older_file)
os.remove(newer_file)
print("Updated the file")




