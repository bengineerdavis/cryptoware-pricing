'''
source: https://stackoverflow.com/questions/57966862/rename-a-column-header-in-csv-using-python-pandas

'''

import pandas as pd
from pathlib import Path
import shutil


files = [file for file in Path("data").iterdir()]
csv_headers = [pd.read_csv(file, nrows=0).columns.tolist() for file in files]
header_dict = dict(zip(files, csv_headers))

naming_dict = dict()
for file, columns in header_dict.items():
    naming_dict[file] = dict()
    for column in columns:
        col = column.lower()
        fname = file.stem.lower()
        # trim dim and fact prefixes from fname for easier atching
        if "dim" in fname:
            fname = fname[4:]
        elif "fact" in fname:
            fname = fname[5:]
        print(f"fname: {fname}")

        if col == "id":
            new_col_name = "id"
        elif ("id" in col and fname[:3] in {"cpu", "gpu", "ram"} and "prod" in col):
            f_table = fname[:3]
            prefix = col[:-2]
            new_col_name = f_table + "_" + prefix + "_id"
        elif ("codeid" in col and "crypto" in fname):
            prefix = col[:-2]
            new_col_name = "crypto_data" + "_" + prefix + "_id"
        elif ("id" in col and "id" < col):
            prefix = col[:-2]
            new_col_name = prefix + "_id"
        else:  
            new_col_name = col

        naming_dict[file].update({column: new_col_name})

# for file in files:
#     file2 = Path(f"./output/{file.name}")
#     file2.touch()

for file, rename_pairs in naming_dict.items():
    # file2 = Path(f"./output/{file.name}")
    print(f"rename_pairs: {rename_pairs}")
    df = pd.read_csv(file, nrows=0)
    df.rename(columns = rename_pairs, inplace = True)
    header_row = ','.join(df.columns) + "\n"
    # modify header in csv file
    with open(file, "r+") as f1, open(file, "r+") as f2:
        f1.readline()
        f2.write(header_row)
        shutil.copyfileobj(f1, f2) # copies the data rows