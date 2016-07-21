from census import Census
from us import states
import pandas as pd
from us import states
import os
import psycopg2

'''
    This script pulls census data for the target features for Denver county and inserts them into the AWS RDS.
'''
def census_pull_insert(api_key,db_password):
    c = Census(api_key)

    #connection to AWS RDS
    conn = psycopg2.connect(database='denver', user='postgres', password=db_password,
            host='denverclustering.cfoj7z50le0s.us-east-1.rds.amazonaws.com', port='5432')
    cur = conn.cursor()

    ins = conn.cursor()
    cur.execute("SELECT census_code FROM census_codes;")

    for i in cur:
        census_code = i[0]
        print census_code
        census_data = c.acs.get(('NAME', census_code), geo={'for': 'tract:*', 'in': 'state:%s county:031' % states.CO.fips}, year=2015)
        for tract in census_data:
            value = tract[census_code]
            tract = tract['NAME'].split(',', 1)[0].split()[-1]
            ins.execute("INSERT INTO census_info (census_code, value, census_tract, yr) VALUES (%s, %s, %s, 2015);", (census_code,value,tract))
            conn.commit()
        # print census_data[0][census_code], census_data[0]['tract']

    cur.close()
    ins.close()
    conn.close()


if __name__ == '__main__':

    api_key = os.environ['CENSUS_API']
    #import password for AWS RDS
    db_password = os.environ['AWS_DENVER_POSTGRES']

    census_pull_insert(api_key,db_password)
