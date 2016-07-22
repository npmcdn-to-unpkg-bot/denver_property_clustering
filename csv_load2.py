import psycopg2
import pandas as pd
import os
import csv

# password = os.environ['AWS_DENVER_POSTGRES']
#
# conn = psycopg2.connect(database='denver', user='postgres', password=password,
#         host='denverclustering.cfoj7z50le0s.us-east-1.rds.amazonaws.com', port='5432')
#
# cur = conn.cursor()

with open("/Users/michael/Desktop/Denver_Clustering/sales.csv", "rb") as f:
    reader = csv.reader(f, delimiter=",")
    for i, line in enumerate(reader):
        print line
        # print 'line[{}] = {}'.format(i, line)
        # cur.execute("INSERT INTO residential_prop_chars ()
        # conn.commit()
#
# cur.close()
# conn.close()
#
# f.close()


# f = open(r'C:\Users\n\Desktop\data.csv', 'r')
# cur.copy_from(f, temp_unicommerce_status, sep=',')
# f.close()
