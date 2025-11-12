import logging
logging.basicConfig( level=logging.DEBUG)
import json
import random
from pathlib import Path
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import os
import numpy as np
import dataimport.utils.dbutils.qryparsing as d

users=["uweb","uweb","uweb","uweb","uweb","uweb","uweb","zweb","rap1","rap2","rap3","rap3","abc","deva","devb"]
hosts=['bil1','bil2','bil3','bil4','bil5',"dev1","dev2","dev3","adm1","web1","web1","web1","web1","web1","web2","web2","web2","web3","web3","web3"]
programs=['program1','program1','program1','program1','program1',"dbeaver","dbeaver","dbeaver","psql"]
databases=['forwebdb','appstandarddb','archdb','testdb']
def load_config(path: str  ="../../cfg/config.json", section: str = "postgresql") -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Nie znaleziono pliku konfiguracyjnego: {path}")

    if section not in cfg:
        raise KeyError(f"Sekcja '{section}' nie istnieje w {path}")

    return cfg[section]


def build_connection_url(cfg: dict) -> str:

    dialect = cfg.get("dialect", "postgresql")
    driver = cfg.get("driver", "psycopg2")
    user = cfg["user"]
    password = cfg["password"]
    host = cfg.get("host",  cfg["host"])
    port = cfg.get("port", 5432)
    database = cfg["database"]

    return f"{dialect}+{driver}://{user}:{password}@{host}:{port}/{database}"

def getTables (prfx,max) :
    str1="trnd_"
    ret= {}
    prefixes = [
        "","dim", "fact", "tmp", "stg", "raw", "hist", "agg", "cfg", "ref", "log"
    ]
    subjects = [
        "sales", "orders", "customers", "transactions", "products", "calendar",
        "inventory", "shipments", "payments", "users", "events", "sessions",
        "metrics", "analytics", "finance", "weather", "tournaments", "players","ledger","bil01","bil02","bil03","bil04","bil05"
    ]
    suffixes = [
        "","a","b","c", "data", "rcrds", "det", "hst", "smm", "daily", "monthly", "arch"

    ]
    r=random.randrange(0,20)
    i=0
    for e1 in prefixes:
        for e2 in suffixes:
            for e3 in subjects:
                tbnm=e1+"_"+e2+"_"+e3
                tbnm = prfx+tbnm.lstrip("_").rstrip("_").replace("__","_")
                clms=getColumns(1,10)
                ret[tbnm]={'c':clms}
                i+=1
                if i > max :
                    return ret
    return ret

def getColumns (c1,c2) :
    str1="trnd_"
    ret=[]
    prefixes = [
        "a","b",""
    ]
    subjects = [
        "dt", "dts", "cid", "tiden", "pid", "xid",
        "val1", "val2", "acc1", "acc2", "usr", "sess"
    ]
    suffixes = [
        "","a","b","c"

    ]
    i=0
    for e1 in prefixes:
        for e2 in suffixes:
            for e3 in subjects:
                cnm=e1+"_"+e2+"_"+e3
                cnm = cnm.lstrip("_").rstrip("_").replace("__","_")

                ret.append(cnm)
                if i>c1 :
                    ret.append(cnm)
                i+=1

                if i > c2 :
                    return ret
    return ret

def getQueries (tabs,qmax ) :
    ret=[]
    symbols=['=','=','=','=','=','=','=','=','=','=','=','<','>',"!="]
    for i in range (0,qmax) :
        ntabs=random.randint(1,4)
        sbf="SELECT "
        fbf=" FROM "
        wbf=" WHERE "
        wpairs=["VAL","VAL","VAL","VAL","VAL","VAL"]
        for j in range(0,ntabs) :

            tab=random.choice(list(tabs))
            fbf += " {} as a{},".format(tab, j)
            print ("-",i,ntabs,j,tab)
            r1=random.randint(2,5)
            r2= random.randint(4, 50)
            for i1 in range(0,r1) :
                sbf+=" a{}.{},".format(i1,random.choice(tabs[tab]['c']))
            for i2 in range(0, r2):
                wpairs.append("a{}.{}".format(i1,random.choice(tabs[tab]['c'])))



        r3= random.randint(4, 8)
        for i3 in range(1,r3) :
            wbf+=" {} {} {} and ".format(random.choice(wpairs),random.choice(symbols),random.choice(wpairs))
        qbg = sbf.rstrip(",") + fbf.rstrip(",") + wbf.rstrip("and ")
        print(qbg)
        ret.append(qbg)
    return ret




def writeQueriesToFile(flnm):
    tabs = getTables("t0_", 200)
    qrs = getQueries(tabs, 25000)

    qout = open(flnm, 'w')
    for q in qrs:
        qout.write(q + "\n")
def generateRows (flnm,dt, size) :
    ret=[]
    mu, sigma = 1, 200.  # mean and width
    #size = 50000
    data = np.random.normal(mu, sigma, size)
    qin=open(flnm,'r')
    qrs=[]
    for ln in qin :
        qrs.append(ln.rstrip())

    maxv=np.max(data)
    coff=1
    if maxv > len(qrs) :
        coff=len(qrs)/maxv
    for i in data :
        idx=int(abs(i)*coff)
        tm="{:02d}{:02d}".format(random.randint(0,23),random.randint(0,59))
        insbf="'{}','{}','{}','{}','{}','{}','{}','{}',0".format(qrs[idx][:255],dt,tm,random.choice(users),random.choice(databases),random.choice(hosts),random.choice(programs),random.randint(1000,100000))

        insbf="INSERT INTO stmt.stmt_indata ( nqry, dt, tm, unm, dnm, hnm, xnm, sesnum, status) VALUES ("+insbf +")"
        #print(insbf)
        ret.append(insbf)
    return ret

def saveRows (engine, qrys ):
    cnt=0
    with engine.connect() as conn:
        for qry in qrys :
            row = conn.execute(text(qry))
            cnt+=1
            #print(len(qrys),cnt,row.rowcount)
        print(len(qrys), cnt)
        conn.commit()
def main():

    print(Path.cwd())
    print(os.environ)
    print("-------------------")

    config = load_config()
    db_url = build_connection_url(config)
    print (db_url)
    try:
        engine = create_engine(db_url)

        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.scalar()
            print("Connection  OK →", version)
        #writeQueriesToFile("../../data/queries.txt")
            result = conn.execute(text("SELECT dt,calendardayinweek, calendardayinmonth from stmt.dim_calendar where dt>'2024-01-02' and dt< now() and dt not in (select dt from stmt.stmt_fact);"))
            for row in result:

                dt=row[0].strftime('%Y-%m-%d')
                size=random.randint(8000,11000)+7-int(row[1])*random.randint(10,900)
                if int(row[2]) <4 :
                    size+=random.randint(2000,3500)
                print (dt,size)
                rows=generateRows("../../data/queries.txt",dt,size)
                saveRows(engine,rows)
                d.parsingNewRecordsDictionary(engine)
                d.parsingNewRecordsHistory(engine, {'clean': 1})
    except SQLAlchemyError as e:
        print("ERROR SQLAlchemy:", e)



if __name__ == "__main__":
    main()