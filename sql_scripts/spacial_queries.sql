--Update Census Tract For Each Parcel
update parcels h set census_tract_name = 'Census Tract 43.02' where
h.gid in (
Select gid
from (
Select p.gid,ST_Contains(t.geom,p.geom)
from (select tract_name, geom from census_tracts where tract_name = 'Census Tract 43.02') t, (
Select gid, geom
from parcels where gid not in (5616,5890,5926,
22064,62113,118975,157455,166657,170534,173688,174462,183480,187054,195921,
199367,199370,199372,201721,204186,205291,206744,211041,211070,211301,211464,
211655,211656,212703,212815,213588,214906,218250,219847,219920,224367,224908)) p ) r
Where ST_Contains = 't');

--How many liquor stores within 2000 meters
SELECT liqlic.*
   FROM liqlic INNER JOIN parcels
      ON ST_DWithin(ST_Transform(liqlic.geom,2232), ST_Transform(parcels.geom,2232), 1000)
WHERE parcels.gid = 176899;
