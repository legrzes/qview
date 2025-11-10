from qvweb.models import *
from django.db.models import Count, Sum, QuerySet
from django.db import connection
import datetime

FROMDT="2024-01-01"

def getQueries(f,v,dt=FROMDT) :

    s=StmtFact.objects.values('qid').filter(**{f:v},dt__gte=dt).annotate(duration=Sum('cnt')).order_by('-duration')[:20]

    ret=[]
    for i in s:
        o=StmtQry.objects.get(id=i['qid'])
        ret.append({'qid':i['qid'],'qnm':o.nqry,'drt':i['duration']})

    return ret

def getUsers(f,v,days=365) :
    dt= datetime.date.today() - datetime.timedelta(days=days)
    if (v>0) :
        s=StmtFact.objects.values('uid').filter(**{f:v},dt__gte=dt).annotate(duration=Sum('cnt')).order_by('-duration')
    else :
        s = StmtFact.objects.values('uid').filter( dt__gte=dt).annotate(duration=Sum('cnt')).order_by('-duration')
    ret=[]
    for i in s:
        o=StmtUser.objects.get(id=i['uid'])
        #print (u)
        ret.append({'uid':i['uid'],'unm':o.unm,'drt':i['duration']})

    return ret

def getHosts(f,v,days=365) :
    dt= datetime.date.today() - datetime.timedelta(days=days)
    s=StmtFact.objects.values('hid').filter(**{f:v},dt__gte=dt).annotate(duration=Sum('cnt')).order_by('-duration')

    ret=[]
    for i in s:
        o=StmtHost.objects.get(id=i['hid'])
        #print (u)
        ret.append({'hid':i['hid'],'hnm':o.hnm,'drt':i['duration']})

    return ret
def getPrograms(f,v,days=365) :
    dt= datetime.date.today() - datetime.timedelta(days=days)
    s=StmtFact.objects.values('xid').filter(**{f:v},dt__gte=dt).annotate(duration=Sum('cnt')).order_by('-duration')

    ret=[]
    for i in s:
        o=StmtPrgm.objects.get(id=i['xid'])
        #print (u)
        ret.append({'xid':i['xid'],'xnm':o.xnm,'drt':i['duration']})

    return ret

def getDbs(f,v,days=365) :
    dt= datetime.date.today() - datetime.timedelta(days=days)
    s=StmtFact.objects.values('did').filter(**{f:v},dt__gte=dt).annotate(duration=Sum('cnt')).order_by('-duration')
    #print ("SSS",qid, s)
    ret=[]
    for i in s:
        o=StmtDb.objects.get(id=i['did'])
        #print (u)
        ret.append({'did':i['did'],'dnm':o.dnm,'drt':i['duration']})

    return ret
def getQryExpl(qid) :


    s = StmtQryExmpl.objects.filter(qid=qid)
    print ("getQryExpl",qid, s)
    ret=[]
    for i in s:
        print ("i",i)
        print("i", i.id)
        ret.append({'eid':i.id,'dttm':i.dttm,'stxt':i.stxt})

    return ret

def getQryExpl(qid) :
    #values('qid').annotate(duration=Sum('cnt')).order_by('-duration')

    s = StmtQryExmpl.objects.filter(qid=qid)
    print ("getQryExpl",qid, s)
    ret=[]
    for i in s:
        print ("i",i)
        print("i", i.id)
        ret.append({'eid':i.id,'dttm':i.dttm,'stxt':i.stxt})

    return ret

def getStmtDrtBy(f,v,fld):
    xset=[]
    yset=[]
    with connection.cursor() as cursor:


        if (v>0) :
            cursor.execute("SELECT "+fld+", sum(cnt)  as drt FROM stmt.stmt_fact sf, stmt.dim_calendar dc WHERE sf.dt =dc.dt and sf."+f+"=%s group by "+fld+" order by "+fld, [v])
        else :
            cursor.execute("SELECT "+fld+", sum(cnt)  as drt FROM stmt.stmt_fact sf, stmt.dim_calendar dc WHERE sf.dt =dc.dt group by " + fld + " order by " + fld)
        for row in cursor:
            xset.append(row[0])
            yset.append(row[1])

    return xset,yset

def getStmtAvrDrtBy(f,v,fld,days=365):
    from_date = datetime.date.today() - datetime.timedelta(days=days)
    xset=[]
    yset=[]
    with connection.cursor() as cursor:
        if (v>0) :
            cursor.execute("select "+fld+", avg(drt)  as drt from (select "+fld+", sf.dt, sum(cnt) as drt   from stmt.stmt_fact sf, stmt.dim_calendar dc where sf.dt=dc.dt and "+f+"=%s  and sf.dt>=%s  group by "+fld+", sf.dt) group by "+fld+" order by "+fld +" asc", [v,from_date])
        else :
            cursor.execute(
                    "select " + fld + ", avg(drt)  as drt from (select " + fld + ", sf.dt, sum(cnt) as drt   from stmt.stmt_fact sf, stmt.dim_calendar dc where sf.dt=dc.dt  and sf.dt>=%s  group by " + fld + ", sf.dt) group by " + fld + " order by " + fld + " asc",
                    [from_date])
        for row in cursor:
            xset.append(row[0])
            yset.append( float(row[1]))
    #print(connection.queries[-1])

    return xset,yset
def getStmtAvrDrtByHour(f,v,days=365):
    from_date = datetime.date.today() - datetime.timedelta(days=days)
    xset=[]
    yset=[]
    with connection.cursor() as cursor:
        if v>0 :
            cursor.execute("select hr,avg(drt) from  ( select hr, dt , sum(cnt ) as drt from stmt.stmt_fact where "+f+"=%s and dt>=%s group by hr,dt ) group by hr order by hr asc",[v,from_date])
        else:
            cursor.execute("select hr,avg(drt) from  ( select hr, dt , sum(cnt ) as drt from stmt.stmt_fact where dt>=%s group by hr,dt ) group by hr order by hr asc",[from_date])

        for row in cursor:
            xset.append(row[0])
            yset.append( float(row[1]))

    return xset,yset
def getDataSets(f,v,days=365) :
    xset1=[]
    yset1=[]
    from_date = datetime.date.today() - datetime.timedelta(days=days)
    if v>0 :
        rslc1 = StmtFact.objects.filter( **{f:v} , dt__gte =  from_date).values('dt').annotate(drt=Sum('cnt')).order_by('dt')
    else:
        rslc1 = StmtFact.objects.filter(dt__gte=from_date).values('dt').annotate(drt=Sum('cnt')).order_by('dt')
    for r in rslc1:
        xset1.append(r['dt'].strftime('%Y-%m-%d'))
        yset1.append(r['drt'])
    return xset1,yset1,days,from_date.strftime('%Y-%m-%d')