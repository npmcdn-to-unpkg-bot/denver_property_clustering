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

--How many liquor stores within .75 miles/3960 feet
SELECT liqlic.*
   FROM liqlic INNER JOIN parcels
      ON ST_DWithin(ST_Transform(liqlic.geom,2232), ST_Transform(parcels.geom,2232), 3960)
WHERE parcels.gid = 176899;

--Sales in .75 miles/3960 feet
select *
from pin_dates p
left join sales s
	on p.pin = s.pin and p.monthd = s.sale_monthd
Where p.monthd > '01/01/2015'
and s.pin in (SELECT p2.pin
   FROM parcels p INNER JOIN parcels p2
      ON ST_DWithin(ST_Transform(p.geom,2232), ST_Transform(p2.geom,2232), 1000)
WHERE p.gid = 176899);



    update pin_dates set sales_count = sale_agg.sale_count
    from (
        select sale_monthd, count(*) as sale_count, p.pin
        from pin_dates p
            left join sales s
                on p.pin = s.pin and p.monthd = s.sale_monthd
        Where s.pin in (SELECT p2.pin
                        FROM parcels p
                            INNER JOIN parcels p2 ON ST_DWithin(ST_Transform(p.geom,2232), ST_Transform(p2.geom,2232), 3960)
                            WHERE p.gid = %s)
        and sale_monthd >= '1/1/2010' and sale_monthd < '1/1/2011'
        group by sale_monthd, p.pin ) sale_agg
    Where pin_dates.monthd = sale_agg.sale_monthd and pin_dates.pin = sale_agg.pin;



        select *
        from pin_dates p
            left join sales s
            on p.pin = s.pin and p.monthd = s.sale_monthd
        Where s.pin in (SELECT p2.pin
                        FROM parcels p
                            INNER JOIN parcels p2 ON ST_DWithin(ST_Transform(p.geom,2232), ST_Transform(p2.geom,2232), 3960)
                            WHERE p.gid = 2345)
        and sale_year = '2010'
        group by sale_monthd, p.pin
