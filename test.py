import pandas as pd
import numpy as np
import psycopg2
import os


db_password = os.environ['AWS_DENVER_POSTGRES']

conn = psycopg2.connect(database='denver', user='postgres', password=db_password,
        host='denverclustering.cfoj7z50le0s.us-east-1.rds.amazonaws.com', port='5432')

cursor = conn.cursor()
cursor.execute("Select distinct census_code, value, census_tract, p.monthd from (select distinct monthd from pin_dates where monthd >= '1/1/2010' and monthd < '1/1/2016') p left join (select census_code, value, census_tract, monthd from census_info where census_tract = '%s') ci on p.monthd = ci.monthd;",(45.05,))
census_df =pd.DataFrame(cursor.fetchall(),columns=['census_code','value','census_tract', 'monthd'])
cursor.close()
conn.close()


pivoted_census_df = census_df.pivot(index='monthd',columns='census_code',values='value')
census_dataframe = pivoted_census_df.reset_index()
census_dataframe['census_tract'] = 45.05


df10 = census_dataframe[:12]
df10 = df10.fillna(method='bfill')
df11 = census_dataframe[11:24]
df11 = df11.interpolate(method='linear')
df12 = census_dataframe[23:36]
df12 = df12.interpolate(method='linear')
df13 = census_dataframe[35:48]
df13 = df13.interpolate(method='linear')
df14 = census_dataframe[47:60]
df14 = df14.fillna(method='bfill')

frames = [df10,df11,df12,df13,df14]
concated_df = pd.concat(frames)
final_df = concated_df.drop_duplicates()
print final_df
