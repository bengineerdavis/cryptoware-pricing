import pandas as pd

from pathlib import Path
from pprint import pformat

'''
Script will define a schema dictionary.
It will then use this schema dictionary to build a SQL file with all of the commands we need
to import CSV data in Postgres
'''


def deconstruct(file):
    '''
    Add key-value pairs decontructed from file data
    Format naming by preferred SQL conventions
    Remove all table prefixes and lowercase table & column names
    '''
    records = pd.read_csv(file, on_bad_lines='skip')
    columns = [record.lower() for record in records.columns]

    file = file.stem.lower()
    if file.startswith('dim_'):
        table = file[len('dim_'):]
    elif file.startswith('fact_'):
        table = file[len('fact_'):]

    # assign each column key to its highest row values
    tables[table] = dict(zip(columns, records.max().tolist()))

def write_to_file(schema):
    '''
    Print the schema dictionary to file schema.py
    '''

    # with open("schema.py", "w+") as f:
    #     pprint(schema, width=70, stream=f)

    output = pformat(schema, sort_dicts=False, width=78)
    with open("schema.py", "w+") as f:
        f.write(output)

    print(output)

    # with open("schema.py", "w+") as f:
    #     f.write(str(pprint(schema, width=70)))


def build_schema(data_dir):
    '''
	Insert tables and datatype clause assignments into schema dictionary
	Write te output of the dictionary into a file
    '''
    global schema, tables
    tables = {}
    data_dir = data_dir.resolve()
    files = [file for file in data_dir.iterdir()]
    for file in files:
        deconstruct(file)
    schema = tables
    for table, pairs in tables.items():
        for column, max_value in pairs.items():
            # foriegn key column clause string
            fk_prefix = column[:-2].lower()
            fk_col_name = fk_prefix + "_id"
            fk_location = fk_prefix + "(id)"
            fk_clause = f"INTEGER REFERENCES {fk_location} ON DELETE CASCADE,"

            # column clause dictionary
            # VARCHAR settings
            bit_length = 128
            # NUMERIC settings
            precision = 20
            decimals = 2
            col_types = {
                "id": "SERIAL",
                "fk": fk_clause,
                # "fk": dict({fk_col_name, fk_clause}),
                "integer": f"INTEGER",
                "numeric": f"NUMERIC({precision},{decimals})",
                "varchar": f"VARCHAR({bit_length})",
                "bool": f"BOOLEAN NOT NULL",
            }
    
            # column clause rules
            id_string = "id"
            # schema[table][column] = {}
            statement = ""
            if (id_string in column and len(id_string) < len(column)) and max_value.is_integer():
                statement = col_types["fk"]
            elif id_string == column:
                statement = col_types["id"]
            elif "is" in column:
                statement = col_types["bool"]
            elif (not isinstance(max_value, float) or isinstance(max_value, int)) and isinstance(max_value, str):
                # default to VARCHAR(128) for text datatypes, for now
                statement = col_types["varchar"]
            elif column not "id" and float(max_value).is_integer():
                statement = col_types["integer"]
            else:
                statement = col_types["numeric"]
  
            schema[table][column] = statement

        write_to_file(schema=schema)


data_dir = Path("data").resolve()

build_schema(data_dir=data_dir)