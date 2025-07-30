select distinct
su.strat_unit_no,
su.map_symbol,
hsu.hydro_subunit_code,
su.strat_name,
hsu.hydro_subunit_desc,
su.map_symbol || hsu.hydro_subunit_code as unit_code,
aq.comments,
aq.created_by,
aq.creation_date,
aq.modified_by,
aq.modified_date
from dd_dh_aquifer_mon aq
join st_strat_unit su on su.strat_unit_no = aq.strat_unit_no
left join wa_hydrostrat_subunit hsu on aq.strat_unit_no = hsu.strat_unit_no and aq.hydro_subunit_code = hsu.hydro_subunit_code
where substr(su.map_symbol, -1) <> upper(substr(su.map_symbol, -1))
order by unit_code