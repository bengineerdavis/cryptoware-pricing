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


#TODO: Use this dict to add in the datatypes into the sqlstamp function
meta_data = {
	"dim_cpu_prod": {
		"Id": "SERIAL",
		"Manufacturer": "VARCHAR(128)",
		"Series": "VARCHAR(128)",
		"CPU_Name": "VARCHAR(128)",
		"Cores": "INTEGER",
		"Socket": "VARCHAR(128)",
		},
	"dim_crypto_data": {
		"Id": "SERIAL",
		"Code": "VARCHAR(128)",
		"Currency_Name": "VARCHAR(128)",
		"Is_Mineable": "BOOLEAN NOT NULL",
		},
	"dim_gpu_prod": {
		"Id": "SERIAL",
		"Processor_Manufacturer": "VARCHAR(128)",
		"Processor": "VARCHAR(128)",
		"GPU_Manufacturer": "VARCHAR(128)",
		"Memory_Capacity": "NUMERIC(7,5)",
		"Memory_Type": "VARCHAR(128)",
		},
	"dim_merchant": {
		"Id": "SERIAL",
		"Merchant": "VARCHAR(128)",
		},
	"dim_ram_prod": {
		"Id": "SERIAL",
		"Manufacturer": "VARCHAR(128)",
		"RAM_Name": "VARCHAR(128)",
		"Memory_Type": "VARCHAR(128)",
		"Speed": "INTEGER",
		"Capacity": "NUMERIC(8,5)",
		},
	"dim_region": {
		"Id": "SERIAL",
		"Code": "VARCHAR(128)",
		"Currency": "VARCHAR(128)",
		},
	"dim_time": {
		"Id": "SERIAL",
		"Year": "INTEGER",
		"Month": "INTEGER",
		"Day": "INTEGER",
		"Week": "INTEGER",
		},
	"fact_cpu_price": {
		"Price_USD": "NUMERIC(18,10)",
		"Price_Original": "NUMERIC(18,10)",
		},
	"fact_crypto_rate": {
		"Open": "NUMERIC(28,6)",
		"Close": "NUMERIC(28,6)",
		"High": "NUMERIC(28,6)",
		"Low": "NUMERIC(28,6)",
		},
	"fact_gpu_price": {
		"Price_USD": "NUMERIC(18,10)",
		"Price_Original": "NUMERIC(18,10)",
		}, 
	"fact_ram_price": {
		"Price_USD": "NUMERIC(18,10)",
		"Price_Original": "NUMERIC(18,10)",
		},
	}



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
				col_end = ","
				space = " "
				# add boilerplate for foreign keys
				foreign_key_clause = " INTEGER REFERENCES " + column[:-2] + "(Id) ON DELETE CASCADE"
				if column in meta_data[table] and meta_data[table][column] is not None:
					data_type = meta_data[table][column]
				# how to handle foriegn key formats and the end of CREATE TABLE statements
				if index == len(columns) - 1 and ("Id" in column and "Id" < column):
					c_string = indent + column + foreign_key_clause
					f.write(c_string + "\n")
					f.write("); " + "\n\n")
				elif index == len(columns) - 1 and not ("Id" in column and "Id" < column):
					c_string = indent + column + space + data_type
					f.write(c_string + "\n")
					f.write("); " + "\n\n")

				elif index != len(columns) - 1 and ("Id" in column and "Id" < column):
					c_string = indent + column + foreign_key_clause + col_end
					f.write(c_string + "\n")
				else:
					c_string = indent + column + space + data_type + col_end
					f.write(c_string + "\n")


target_file = 'schema.sql'# return SQL table metadata
extract(data_dir=target_dir)
sqlstamp(file=target_file)
