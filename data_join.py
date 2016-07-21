import pandas as pd
import numpy as np
import psycopg2
import os

db_password = os.environ['AWS_DENVER_POSTGRES']

conn = psycopg2.connect(database='denver', user='postgres', password=db_password,
        host='denverclustering.cfoj7z50le0s.us-east-1.rds.amazonaws.com', port='5432')
cursor = conn.cursor()

cursor.execute("SELECT census_codes,description FROM census_codes;")


rows=pd.DataFrame(cursor.fetchall(),columns=['page_num','Frequency'])
