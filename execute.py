import hidden

import psycopg2

from pathlib import Path



'''
Run SQL commands in our database

'''
# Load the secrets
secrets = hidden.secrets()

conn = psycopg2.connect(host=secrets['host'],
        database=secrets['database'], 
        user=secrets['user'], 
        password=secrets['pass'], 
        connect_timeout=3)
    
    # add table schemas from sql file
    # source: https://stackoverflow.com/questions/17261061/execute-sql-schema-in-psycopg2-in-python
    cur.execute(
	with open("schema.sql", "r") as sql:
	    sql.read()
	    )
