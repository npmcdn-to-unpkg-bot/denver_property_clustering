import psycopg2
import os

db_password = os.environ['AWS_DENVER_POSTGRES']

conn = psycopg2.connect(database='denver', user='postgres', password=db_password,
        host='denverclustering.cfoj7z50le0s.us-east-1.rds.amazonaws.com', port='5432')
cur = conn.cursor()
cur.execute("CREATE INDEX ON pin_dates (pin);")

conn.commit()
cur.close()
conn.close()
