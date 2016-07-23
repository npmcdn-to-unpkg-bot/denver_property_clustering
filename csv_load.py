import psycopg2
import pandas as pd
import os
import csv

password = os.environ['AWS_DENVER_POSTGRES']

conn = psycopg2.connect(database='denver', user='postgres', password=password,
        host='denverclustering.cfoj7z50le0s.us-east-1.rds.amazonaws.com', port='5432')

cur = conn.cursor()

with open("/Users/michael/Desktop/Denver_Clustering/sales.csv", "rb") as f:
    # reader = csv.reader(f, delimiter=",")
    reader = csv.reader(x.replace('\0', '') for x in f)
    for i, line in enumerate(reader):
        # print 'line[{}] = {}'.format(i, line)
        cur.execute("INSERT INTO sales (schednum,reception_num,instrument,sale_year,sale_monthday,reception_date,sale_price,grantor,grantee,class,mkt_clus,d_class,d_class_cn,nbhd_1,nbhd_1_cn,pin) VALUES (%s, %s, %s,%s,%s,%s, %s, %s,%s,%s,%s, %s, %s,%s,%s,%s);",(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15]))
        conn.commit()

cur.close()
conn.close()

f.close()
