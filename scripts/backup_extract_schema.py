import pandas as pd

# from copy import deepcopy
from pathlib import Path
from pprint import pprint, pformat

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

    pprint(f"table: {table}")
    # assign each column key to its highest row values
    tables[table] = dict(zip(columns, records.max().tolist()))
    pprint(f"schema: {tables}")

def write_to_file(schema):
    '''
    Print the schema dictionary to file schema.py
    '''

    # with open("schema.py", "w+") as f:
    #     pprint(schema, width=70, stream=f)

    output = pformat(schema)
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
    global tables, schema
    schema = {}
    tables = {}
    data_dir = data_dir.resolve()
    files = [file for file in data_dir.iterdir()]
    for file in files:
        deconstruct(file)
    schema = tables.copy()
    for table, pairs in tables.items():
        # fix naming scheme for tables with foreign keys
        for column in pairs.keys():
            # breakpoint()
            fk_prefix = column[:-2].lower()
            fk_col_name = ""
            # translate tables with fk's "ProdId" to format "<table>_prod_id"
            if column != "id" and table[:3] in {"gpu", "cpu", "ram"} and "prod" in column:
                fk_table = table[:3]
                fk_col_name = fk_table + "_" + fk_prefix + "_id"
            elif column != "id" and "crypto" in table and "codeid" == column:
                fk_col_name = "crypto_data" + "_" + fk_prefix + "_id"

            # replace old column name convention with the new one
            schema[table][fk_col_name] = schema[table].pop(column)

        # now select correct datatypes or foreign key clause for each column    
        for column, max_value in pairs.values():
            # breakpoint()
            # column clause string
            # space = " "
            # col_prefix = column + space
            
            # foriegn key column clause string
            fk_prefix = column[:-2].lower()

            # translate tables with fk's "ProdId" to format "<table>_prod_id"
            # if table[:3] in {"gpu", "cpu", "ram"} and "prod" in column:
            #     fk_table = table[:3]
            #     fk_prefix = fk_table + "_" + fk_prefix
            # elif "crypto" in table and "codeid" == column:
            #     fk_prefix = "crypto_data" + "_" + fk_prefix
            # else:
            #     fk_prefix = fk_prefix

            fk_location = fk_prefix + "(id)"
            fk_clause = " INTEGER REFERENCES " + fk_location + " ON DELETE CASCADE"
    

            # column clause dictionary
            bit_length = 128
            precision = len(str(max_value)) + 3
            decimals = 2
            col_types = {
                "id": "SERIAL",
                "fk": dict({fk_col_name: fk_clause}),
                "integer": f"INTEGER",
                "numeric": f"NUMERIC({precision},{decimals})",
                "varchar": f"VARCHAR({bit_length})",
                "bool": f"BOOLEAN NOT NULL",
            }
    
            # column clause rules
            id_string = "id"
            # schema[table][column] = {}
            # statement = ""
            if (id_string in column and id_string < column) and max_value.is_integer():
                print(f"column: {column}")
                for col, clause in col_types["fk"].items():
                    print(f"col: {col}")
                    print(f"clause: {clause}")
                    schema[table][column] = clause
                    schema[table][col] = schema[table].pop(column)
                # column = fk_col_name
            elif (id_string == column and isinstance(max_value, int)):
                schema[table][column] = col_types["id"]
            elif "is" in column:
                schema[table][column] = col_types["bool"]
            elif (not isinstance(max_value, float) or isinstance(max_value, int)) and isinstance(max_value, str):
                # default to VARCHAR(128) for text datatypes, for now
                schema[table][column] = col_types["varchar"]
            elif float(max_value).is_integer():
                schema[table][column] = col_types["integer"]
            else:
                schema[table][column] = col_types["numeric"]
    
            # breakpoint()

        write_to_file(schema=schema)


data_dir = Path("data").resolve()

build_schema(data_dir=data_dir)
