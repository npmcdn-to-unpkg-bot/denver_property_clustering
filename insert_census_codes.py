import psycopg2
import pandas as pd
import os

#import password for AWS RDS
db_password = os.environ['AWS_DENVER_POSTGRES']

#connection to AWS RDS
conn = psycopg2.connect(database='denver', user='postgres', password=db_password,
        host='denverclustering.cfoj7z50le0s.us-east-1.rds.amazonaws.com', port='5432')

cur = conn.cursor()

#create census_codes table on the first run
# try:
#     cur.execute("CREATE TABLE census_codes (id serial PRIMARY KEY, census_code varchar(11),  description varchar(250));")
# except:
#     print 'table already created'

#read codes from text file and prep for inserts
census_codes = pd.read_csv('cencus_codes.txt', sep="|", header = None)
census_codes.columns = ['none','desc','code','none2']
census_codes = census_codes.drop(['none','none2'], axis=1)

# #for each code in census_codes, insert the items to the AWS RDS
for i, code_item in census_codes.iterrows():
    try:
        code = code_item['code']
        code = str(code[:7] + '_' + code[7:-1] + 'E')
        code = code.strip()
        desc = code_item['desc']
        cur.execute("INSERT INTO census_codes (census_code, description) VALUES (%s, %s)", (code,desc))
    except:
        print 'no insert_one'

cur.execute("SELECT * FROM census_codes;")
print cur.fetchone()

conn.commit()
cur.close()
conn.close()
