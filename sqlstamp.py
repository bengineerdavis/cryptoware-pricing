from pathlib import Path
import ast

def sqlstamp(schema_file):
	make_file = target_file = Path('make_tables.sql').resolve() 
	flush_file = "flush.sql"

	# pull in schema dictionary from file
	with open(schema_file, "r") as f:
		data = f.read()

	schema = ast.literal_eval(data)


	with open(flush_file, "w+") as f:
		for table in schema.keys(): 
			drop = f'DROP TABLE IF EXISTS {table} CASCADE;'
			f.write(drop + "\n")
			
	with open(make_file, "w+") as f:
		for table, column_pairs in schema.items():
			counter = 0
			number_of_columns = len(column_pairs.keys())
			prefix = "CREATE TABLE " + table + " ("
			f.write(prefix + "\n")
			for column, clause in column_pairs.items():
				counter += 1
				# set standard indentation for create table statements
				indent = "    "
				column_string = indent + column + " " + clause
	# 			# how to handle foriegn key formats and the end of CREATE TABLE statements
				if counter >= number_of_columns:
					# remove comma from last column, per PostgreSQL conventions
					f.write(column_string[:-1] + "\n")
					f.write("); " + "\n\n")
				else:
					f.write(column_string + "\n")

		'''
		Create SQL CSV import statements for each file in the data directory to
		pull corresponding file data into their SQL tables
		'''
		files = [file for file in Path("data").iterdir()]
		# pair files with their corresponding SQL tables and create import statements
		import_dict = dict()
		filetype = "CSV"
		for file in files:
			for table in schema.keys():
				if table in file.name.lower():
					import_dict[table] = file
		for table, file in import_dict.items():
			import_file = f"\copy {table}({','.join(column for column in schema[table].keys())}) FROM '{file}' WITH DELIMITER ',' {filetype};"
			f.write(import_file + "\n\n")
	




if __name__ == "__main__":

	schema_file = Path('schema.py').resolve()
	
	sqlstamp(schema_file=schema_file)
	

	
