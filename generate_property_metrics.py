import pandas as pd
import numpy as np
import psycopg2
import os

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
    cur.execute("Select pin from parcels;")

    ins = conn.cursor()

    for i in cur:
        pin = i[0]
        ins.execute('update pin_dates set sales_count = sale_agg.sale_count from (select sale_monthd, count(*) as sale_count, pin as pin from pin_dates p left join sales s on p.pin = s.pin and p.monthd = s.sale_monthd Where s.pin in (SELECT p2.pin FROM parcels p INNER JOIN parcels p2 ON ST_DWithin(ST_Transform(p.geom,2232), ST_Transform(p2.geom,2232), 3960) WHERE p.pin = %s) group by sale_monthd ) sale_agg Where pin_dates.monthd = sale_agg.sale_monthd and pin_dates.pin = sale_agg.pin;',(pin))

# ins.execute('select sale_monthd, count(*) from pin_dates p left join sales s on p.pin = s.pin and p.monthd = s.sale_monthd Where p.monthd > '01/01/2015' and s.pin in (SELECT p2.pin FROM parcels p INNER JOIN parcels p2 ON ST_DWithin(ST_Transform(p.geom,2232), ST_Transform(p2.geom,2232), 1000) WHERE p.pin = %s Group by sale_monthd);',(pin))

    cur.close()
    conn.close()


if __name__ == '__main__':

    #import password for AWS RDS
    db_password = os.environ['AWS_DENVER_POSTGRES']

    propert_level_sales(db_password)
