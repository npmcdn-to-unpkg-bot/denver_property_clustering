import psycopg2
import pandas as pd
import os
from census import Census
from us import states

'''
    Just an example script for creating Postgres DB tables on AWS RDS
'''

def create_table(password):

    conn = psycopg2.connect(database='denver', user='postgres', password=password,
            host='denverclustering.cfoj7z50le0s.us-east-1.rds.amazonaws.com', port='5432')

    cur = conn.cursor()

    cur.execute("CREATE TABLE residential_prop_chars (id serial PRIMARY KEY,PIN varchar(25), SCHEDNUM varchar(25), CD varchar(25), OFCARD varchar(25),OWNER varchar(250),CO_OWNER varchar(250),OWNER_NUM varchar(25),OWNER_DIR varchar(25),OWNER_ST varchar(250),OWNER_TYPE varchar(250),OWNER_APT varchar(250),OWNER_CITY varchar(250),OWNER_STATE varchar(250),OWNER_ZIP varchar(250),SITE_NBR varchar(25),SITE_DIR varchar(250),SITE_NAME varchar(250),SITE_MODE varchar(250),SITE_MORE varchar(250),TAX_DIST varchar(250),PROP_CLASS varchar(25),PROPERTY_CLASS varchar(250),ZONE10 varchar(250),D_CLASS_CN varchar(250),LAND_SQFT varchar(25),AREA_ABG varchar(25),BSMT_AREA varchar(25),FBSMT_SQFT varchar(25),GRD_AREA varchar(25),STORY varchar(25),STYLE_CN varchar(250),BED_RMS varchar(25),FULL_B varchar(25),HLF_B varchar(25),CCYRBLT varchar(25),CCAGE_RM varchar(25),UNITS varchar(25),ASMT_APPR_LAND varchar(25),TOTAL_VALUE varchar(25),ASDLAND varchar(25),ASSESS_VALUE varchar(25),ASMT_TAXABLE varchar(25),ASMT_EXEMPT_AMT varchar(25),NBHD_1 varchar(25),NBHD_1_CN varchar(250),	LEGL_DESCRIPTION varchar(250));")

    conn.commit()
    cur.close()
    conn.close()



if __name__ == '__main__':

    password = os.environ['AWS_DENVER_POSTGRES']
    create_table(password)
