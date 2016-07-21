Select cast(ltrim(census_tract_name,'Census Tract ') as real) as census_tract,tax_dist,land_value,prop_class,total_valu,land,ccyrblt,sale_month,
sale_year,sale_price, gid
from parcels;
