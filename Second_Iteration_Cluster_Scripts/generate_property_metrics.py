import pandas as pd
import numpy as np
import psycopg2
import os
import sys

"""This script is used for property level feature engineering. Spacial queries can be run and data generated for each parcel in the Denver metro area. Monhtly metrics from 01/01/2010 through 12/01/2015 are:

        - Sales count in .75 mile radious
        - Average sale price in .75 mile radious
        - Numer of liquor licenses in .75 mile radious
        - Average home size in .75 mile radious
        - Incidents of crime in .75 mile radious, other than traffic violations

Data is stored in an AWS RDS Portgres instance and accessed via SQL scripts where noted. These files can be acccessed through the project repo. Otherwise inline queries are used.

Author: Michael G Bennett
Create Date: 07/19/2016
Last Update: 07/19/2016

"""
def propert_level_sales_count(db_password):
    #connection to AWS RDS
    conn = psycopg2.connect(database='denver', user='postgres', password=db_password,
            host='denverclustering.cfoj7z50le0s.us-east-1.rds.amazonaws.com', port='5432')
    cur = conn.cursor()
    cur.execute("Select gid,pin from parcels where gid > %s and gid <= %s;",(sys.argv[1],sys.argv[2]))

    ins = conn.cursor()
    printcounter = 0
    for i in cur:
        if (printcounter == 2000):
            print('Progress report.....2000')
            printcounter = 0
        gid = i[0]
        pin = i[1]
        ins.execute("Insert into sales_metrics (monthd, sales_count, avg_price, pin) select sale_monthd, count(*) as sale_count, AVG(cast(NULLIF(sale_price, '10') AS BIGINT)) as avg_price, %s from sales Where pin in (SELECT p2.pin FROM parcels p INNER JOIN parcels p2 ON ST_DWithin(ST_Transform(p.geom,2232), ST_Transform(p2.geom,2232), 3960) WHERE p.gid = %s) group by sale_monthd;",(pin,gid))
        printcounter += 1
        conn.commit()

    cur.close()
    ins.close()
    conn.close()



if __name__ == '__main__':

    #import password for AWS RDS
    db_password = os.environ['AWS_DENVER_POSTGRES']

    propert_level_sales_count(db_password)
