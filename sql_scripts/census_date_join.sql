Select *
from (select distinct monthd from pin_dates) p
    left join census_info ci
        on p.monthd = ci.monthd;
