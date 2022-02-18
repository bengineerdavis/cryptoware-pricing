import pandas as pd

from pathlib import Path

# Define variables for table metadata extraction

schema = dict()
# select target directory with csv files
target_dir = './data'



def extract(data_dir):
	# define paths to CSV files from which we will extract table metadata
	data = Path(target_dir).resolve()
	datasets = [d for d in data.iterdir()]
	# store raw table metadata here
	tables = dict()
	
	
	# create a tables dictionary with columns for the values and table names as the keys
	for ds in datasets:
		tables[ds.stem.lower()] = pd.read_csv(ds.resolve(), on_bad_lines='skip')
	for table in tables:
		schema[table] = [col for col in tables[table].columns]


# return SQL table metadata
extract(data_dir=target_dir)

def sqlstamp(file):
	with open(file, 'w') as f:
		for table, columns in schema.items(): 
			drop = f'DROP TABLE IF EXISTS {table} CASCADE;'
			f.write(drop + "\n")
			prefix = "CREATE TABLE " + table + " ("
			f.write(prefix + "\n")
			for index,column in enumerate(columns):
				c_string = ""
				# set standard indentation for create table statements
				indent = "    "
				# add boilerplate for foreign keys
				foreign_key_clause = " INTEGER REFERENCES " + column[:-2] + "(Id) ON DELETE CASCADE"
				# how to handle foriegn key formats and the end of CREATE TABLE statements
				if index == len(columns) - 1 and ("Id" in column and "Id" < column):
					c_string = indent + column + foreign_key_clause
					f.write(c_string + "\n")
					f.write("); " + "\n\n")
				elif index == len(columns) - 1 and not ("Id" in column and "Id" < column):
					c_string = indent + column
					f.write(c_string + "\n")
					f.write("); " + "\n\n")

				elif index != len(columns) - 1 and ("Id" in column and "Id" < column):
					c_string = indent + column + foreign_key_clause
					f.write(c_string + "\n")
				else:
					c_string = indent + column + ","
					f.write(c_string + "\n")


target_file = 'schema.sql'

sqlstamp(file=target_file)
