SELECT dh.drillhole_no AS dh_no, --col
       To_char(dh.map_100000_no)
              || '-'
              || To_char(dh.dh_seq_no) AS unit_hyphen, --col
       Trim(To_char(dh.obs_well_plan_code))
              || Trim(To_char(dh.obs_well_seq_no, '000')) AS obs_no,  --col
       dh.dh_name                                         AS dh_name, --col
       summ.aq_subaq                                      AS aquifer, --col
       f.file_no,
       f.file_name,
       f.file_type_code,
       f.comments,
       f.file_doc_type_code,
       f.file_date,
       f.gl_auto_sync_flag,
       f.created_by,
       f.creation_date,
       f.modified_by,
       f.modified_date
FROM   dhdb.fi_file f
join   dhdb.fi_file_link_vw fi
ON     f.file_no = fi.file_no
join   dhdb.dd_drillhole_vw dh
ON     fi.drillhole_no = dh.drillhole_no
join   dhdb.dd_drillhole_summary_vw summ
ON     dh.drillhole_no = summ.drillhole_no
WHERE  dh.drillhole_no IN {DH_NO} --arg DH_NO (sequence of int): drillhole numbers or a :class:`pandas.DataFrame` with a "dh_no" column
AND    dh.deletion_ind = 'N'