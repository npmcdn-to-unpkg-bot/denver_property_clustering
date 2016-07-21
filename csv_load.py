import psycopg2
import pandas as pd
import os
import csv

password = os.environ['AWS_DENVER_POSTGRES']

conn = psycopg2.connect(database='denver', user='postgres', password=password,
        host='denverclustering.cfoj7z50le0s.us-east-1.rds.amazonaws.com', port='5432')

cur = conn.cursor()

with open("/Users/michael/Desktop/Denver_Project/real_property_residential_chars2.csv", "rb") as f:
    # reader = csv.reader(f, delimiter=",")
    reader = csv.reader(x.replace('\0', '') for x in f)
    for i, line in enumerate(reader):
        # print 'line[{}] = {}'.format(i, line)
        print line[0]
        if i > 64445:
            cur.execute("INSERT INTO residential_prop_chars (pin ,schednum,cd,ofcard,owner,co_owner,owner_num,owner_dir ,owner_st ,owner_type,owner_apt ,owner_city ,owner_state ,owner_zip,site_nbr ,site_dir ,site_name ,site_mode ,site_more ,tax_dist ,prop_class , property_class ,zone10 ,d_class_cn ,land_sqft ,area_abg ,bsmt_area ,fbsmt_sqft ,grd_area ,story ,style_cn ,bed_rms ,full_b ,hlf_b ,ccyrblt ,ccage_rm ,units ,asmt_appr_land ,total_value ,asdland ,assess_value ,asmt_taxable,asmt_exempt_amt,nbhd_1, nbhd_1_cn,legl_description) VALUES (%s, %s, %s,%s,%s,%s, %s, %s,%s,%s,%s, %s, %s,%s,%s,%s, %s, %s,%s,%s,%s, %s, %s,%s,%s,%s, %s, %s,%s,%s,%s, %s, %s,%s,%s,%s, %s, %s,%s,%s,%s, %s, %s,%s,%s,%s);",(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],line[28],line[29],line[30],line[31],line[32],line[33],line[34],line[35],line[36],line[37],line[38],line[39],line[40],line[41],line[42],line[43],line[44],line[45]))
            conn.commit()
        else:
            pass

cur.close()
conn.close()

f.close()
