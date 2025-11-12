from sqlalchemy import select, engine
from sqlalchemy.orm import Session
import sqlalchemy as db
import utils.dbutils.stmtmodels as m
from sqlalchemy import text


def parsingNewRecordsDictionary (en ):
    """
    Function takes data from stmt_indata and produce dictionary items and putting them in respective table
    :param en:
    :return:
    """
    metadata = db.MetaData()
    session = Session(en)
    sql01="""
    update stmt.stmt_indata set nqry='-' where nqry is null;
    update stmt.stmt_indata set unm='-' where unm is null;
    update stmt.stmt_indata set hnm='-' where hnm is null;
    update stmt.stmt_indata set xnm='-' where xnm is null;
    update stmt.stmt_indata set dnm='-' where dnm is null;

    """
    sql1="insert into stmt.stmt_qry (nqry) select distinct nqry  from stmt.stmt_indata where nqry not in (select nqry from stmt.stmt_qry) ; "
    sql2="insert into stmt.stmt_user (unm) select distinct lower(unm) from stmt.stmt_indata where lower(unm) not in (select lower(unm) from stmt.stmt_user);"
    sql3 = "insert into stmt.stmt_host ( hnm) select distinct lower(hnm) from stmt.stmt_indata where lower(hnm) not in (select lower(hnm) from stmt.stmt_host);"
    sql4 = "insert into stmt.stmt_prgm ( xnm) select distinct lower(xnm) from stmt.stmt_indata where lower(xnm) not in (select lower(xnm) from stmt.stmt_prgm);"
    sql5 = "insert into stmt.stmt_db ( dnm) select distinct lower(dnm) from stmt.stmt_indata where lower(dnm) not in (select lower(dnm) from stmt.stmt_db);"
    sql6 = "insert into stmt.stmt_srv ( snm) select distinct lower(server) from stmt.stmt_indata where lower(server) not in (select lower(snm) from stmt.stmt_srv);"


    #print (stmt)
    with en.connect() as conn:
        row = conn.execute(text(sql01))
        print("SQL01",row.rowcount)
        row = conn.execute(text("commit"))
        row=conn.execute(text(sql1))
        print(row.rowcount)
        row=conn.execute(text(sql2))
        print(row.rowcount)
        row = conn.execute(text(sql3))
        print(row.rowcount)
        row = conn.execute(text(sql4))
        print(row.rowcount)
        row = conn.execute(text(sql5))
        print(row.rowcount)
        row = conn.execute(text(sql6))
        print(row.rowcount)

def parsingNewRecordsHistory (en , opt={}):
    print (opt)
    sqlH = """
        insert into stmt.stmt_fact (qid,dt,hr,uid,did,hid,xid,cnt,sid)
    select q.id,i.dt, substr(i.tm,0,3)::int as hr, u.id as uid, d.id as did, h.id as hid, x.id as xid, count(*) as cnt, s.id as sid
    from stmt.stmt_indata i
     join stmt.stmt_qry q on i.nqry=q.nqry
     join stmt.stmt_user u on i.unm=u.unm
     join stmt.stmt_db d on i.dnm=d.dnm
     join stmt.stmt_host h on i.hnm=h.hnm
     join stmt.stmt_prgm x on i.xnm=x.xnm
     join stmt.stmt_srv s on i.server=s.snm
     where i.status=0
    group by q.id, dt,hr,uid,did,hid,xid, sid
            """
    with en.connect() as conn:
        row = conn.execute(text(sqlH))
        print(row.rowcount)

        if 'clean' in opt and opt['clean']==1 :
            print ("cleaning")
            row = conn.execute(text("delete from stmt.stmt_indata"))
            print ("cleaned|records=",row.rowcount)
        if 'setstatus' in opt :
            row = conn.execute(text("update  stmt.stmt_indata set status={}".format(opt['setstatus'])))
        conn.commit()

def parsingNewQryExamples (en: engine , opt={}):
    sqlH = """
        insert into stmt.stmt_qry_exmpl (qid,dttm,stxt)
    select q.id,i.dt, i.fqry
    from stmt.stmt_inexmpl i
     join stmt.stmt_qry q on i.nqry=q.nqry
     where i.status=0
            """
    ret=[]
    with en.connect() as conn:
        row = conn.execute(text(sqlH))
        print(row.rowcount)
        ret.append(row.rowcount)
        if 'clean' in opt and opt['clean']==1 :
            row = conn.execute(text("delete from stmt.stmt_inexmpl"))
            print(row.rowcount)
            ret.append(row.rowcount)
        if 'setstatus' in opt :
            sql="update  stmt.stmt_inexmpl set status="+str(opt['setstatus'])
            row = conn.execute(text(sql))
            print(sql,row.rowcount)
            ret.append(row.rowcount)
        conn.commit()


    return ret