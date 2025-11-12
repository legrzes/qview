#!/bin/sh

DT=`date +'%Y%m%d'`
TM=`date +'%H%M%S'`
expfl=~/pg/monitor/pg_qry_activity.$DT.txt
expflrepl=~/pg/monitor/pg_qry_replication.$DT.txt
echo "INFO pg_stat_activity $DT $TM" >> $expfl
echo "select * FROM pg_catalog.pg_stat_activity where state='active'" | psql -t -U user1  test2 >> $expfl

