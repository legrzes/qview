Scripts which can be used to ingest data.

1.
Colecting data from PG :
* * * * * /home/USER/pg/bin/pg_qry_dump_cron.sh
2. Scripts dump queries to file pg_qry_activity.YYYYMMDD.txt
3. Parsing using import_pg.py (you can use script
   bin/import_pg.py PATH/pg_qry_activity.YYYYMMDD.txt
4. Load to stage database:
echo " COPY stmt.stmt_indata ( nqry, dt, tm, unm, dnm, hnm, xnm, sesnum, status, server) FROM '/tmp/pg_qry_activity.all.in' DELIMITER '|' CSV ; " | psql -t -U tuser1 test2
echo " COPY stmt.stmt_inexmpl ( dt, nqry, fqry) FROM '/tmp/pg_qry_activity.all.sdb' DELIMITERS E'\t' CSV ; " | psql -t -U tuser1 test2





requirements:
psycopg2-binary
sql-metadata
sqlalchemy
numpy
matplotlib