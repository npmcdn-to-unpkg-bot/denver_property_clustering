from census import Census
from us import states
import pandas as pd
from us import states
import os
import psycopg2

def update_tracts(db_password):

    #connection to AWS RDS
    conn = psycopg2.connect(database='denver', user='postgres', password=db_password,
            host='denverclustering.cfoj7z50le0s.us-east-1.rds.amazonaws.com', port='5432')
    cur = conn.cursor()

    cur.execute("SELECT tract_name FROM census_tracts;")

    ins = conn.cursor()

    for i in cur:
        tract = str(i[0])
        print tract
        ins.execute("update parcels h set census_tract_name = %s where h.gid in (Select gid from (Select p.gid,ST_Contains(t.geom,p.geom) from (select tract_name, geom from census_tracts where tract_name = %s) t, (Select gid, geom from parcels where gid not in (5616,5890,5926,22064,62113,118975,157455,166657,170534,173688,174462,183480,187054,195921,199367,199370,199372,201721,204186,205291,206744,211041,211070,211301,211464,211655,211656,212703,212815,213588,214906,218250,219847,219920,224367,224908)) p ) r Where ST_Contains = 't');", (tract,tract))
        conn.commit()

    cur.close()
    ins.close()
    conn.close()



if __name__ == '__main__':

    #import password for AWS RDS
    db_password = os.environ['AWS_DENVER_POSTGRES']

    update_tracts(db_password)
