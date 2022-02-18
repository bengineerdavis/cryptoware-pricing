def secrets():
    return {"host": "localhost",
            "database": "ethereum",
            "user": "lore",
            "pass": "philben"}

def psycopg2(secrets) :
     return ('dbname='+secrets['database']+
	     ' user='+secrets['user']+
	     ' password='+secrets['pass']))

