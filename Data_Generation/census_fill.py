from census import Census
from us import states
import pandas as pd
from us import states
import os
import psycopg2


api_key = os.environ['CENSUS_API']

c = Census(api_key)

census_data = c.acs.get(('NAME', 'B01001_003E'), geo={'for': 'tract:*', 'in': 'state:%s county:031' % states.CO.fips}, year=2013)

print census_data
