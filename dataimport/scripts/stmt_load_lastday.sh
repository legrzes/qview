#!/bin/sh


DTPREV=`date -d "yesterday" +"%Y%m%d"`

echo DTPREV=$DTPREV

FLDIR=$HOME/pg/monitor/
FLNM=pg_qry_activity.$DTPREV.txt

cd $HOME/pg/qry_stat/
source .venv/bin/activate
python3 bin//import_pg.py $FLDIR/$FLNM srvtest1 > $FLDIR/$FLNM.import_pg
cp   $FLDIR/$FLNM.sdb    $FLDIR/$FLNM.in /tmp/
echo INRAPRECORDS=`cat $FLDIR/$FLNM |wc -l` IN_RECORDS=`cat $FLDIR/$FLNM.in |wc -l ` SDB_RECORDS=`cat $FLDIR/$FLNM.sdb|wc -l`
echo " COPY stmt.stmt_indata ( nqry, dt, tm, unm, dnm, hnm, xnm, sesnum, status,server) FROM '/tmp/$FLNM.in' DELIMITER '|' CSV ; " | psql -t -U user1 test2
echo " COPY stmt.stmt_inexmpl ( dt, nqry, fqry) FROM '/tmp/$FLNM.sdb' DELIMITERS E'\t' CSV ; " | psql -t -U user1 test2
