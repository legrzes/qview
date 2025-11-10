from django.db.models.expressions import result
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count, Sum, QuerySet, Max, Avg
from django.core.paginator import Paginator
from .models import *
from django.views.generic.list import ListView
import  qvweb.utils.dbutils as  du
import datetime
from django.db import connection
# Create your views here.

def index(request):
    rec={}
    inf={}
    inf['lastdt']=StmtFact.objects.aggregate(latest=Max('dt'))['latest']
    print (inf['lastdt'])



    rec['xset1'], rec['yset1'], rec['days1'], rec['fromDt1'] = du.getDataSets("", -1, 500)
    rec['xset2'], rec['yset2'], rec['days2'], rec['fromDt2'] = du.getDataSets("", -1, 30)
    rec['xset3'], rec['yset3'], rec['days3'], rec['fromDt3'] = du.getDataSets("", -1, 7)
    rec['xset_hr'], rec['yset_hr'] = du.getStmtAvrDrtByHour("", -1)
    rec['xset_di_w'],rec['yset_di_w']= du.getStmtAvrDrtBy("",-1,'calendardayinweek')
    rec['xset_di_m'], rec['yset_di_m'] = du.getStmtAvrDrtBy("",-1, 'calendardayinmonth')

    from_date1 = datetime.date.today() - datetime.timedelta(days=1)
    rec['q'] = StmtFact.objects.filter( dt__gte =  from_date1).annotate(drt=Sum('cnt')).order_by('-drt')
    rec['u'] = du.getUsers("",-1,365)
    # rec['d'] = du.getDbs(qidx)
    # rec['x'] = du.getPrograms(qidx)
    # rec['h'] = du.getHosts(qidx)
    return render(request, "index.html", {'oinf': { 'inf':inf, 'rec':rec }} )

def topQueries(request):
    rslc = StmtFact.objects.values('qid').annotate(drt=Sum('cnt')).order_by('-drt')[:50]
    result=[]
    lc=0
    for r in rslc:

        rec={}
        lc+=1
        rec['lc']=lc
        rec['drt'] = r['drt']
        rec['q'] = StmtQry.objects.get(id=r['qid'])
        rec['u'] = du.getUsers('qid',r['qid'])
        rec['d'] = du.getDbs('qid',r['qid'])
        rec['x'] = du.getPrograms('qid',r['qid'])
        rec['h'] = du.getHosts('qid',r['qid'])
        result.append(rec)
    return render(request, "top_queries.html",{'result':result})

def userInfo(request, idx):
    fldid = "uid"
    inf = {'fldid':fldid,'itemtype':'User'}
    lc=0


    rec={}
    lc+=1
    rec['lc']=lc

    rec['i'] = StmtUser.objects.get(id=idx)
    #rec['u'] = du.getUsers(fldid,idx)
    rec['q'] = du.getQueries(fldid, idx)
    rec['d'] = du.getDbs(fldid,idx)
    rec['x'] = du.getPrograms('uid',idx)
    rec['h'] = du.getHosts(fldid,idx)


    rec['xset1'], rec['yset1'], rec['days1'], rec['fromDt1'] = du.getDataSets(fldid, idx, 500)
    rec['xset2'], rec['yset2'], rec['days2'], rec['fromDt2'] = du.getDataSets(fldid, idx, 30)
    rec['xset3'], rec['yset3'], rec['days3'], rec['fromDt3'] = du.getDataSets(fldid,idx,7)

    rec['xset_hr'],rec['yset_hr']=du.getStmtAvrDrtByHour(fldid,idx)
    rec['xset_di_w'],rec['yset_di_w']= du.getStmtAvrDrtBy(fldid,idx,'calendardayinweek')
    rec['xset_di_m'], rec['yset_di_m'] = du.getStmtAvrDrtBy(fldid,idx, 'calendardayinmonth')

    return render(request, "itemInfo.html", {'oinf': {'inf':inf, 'rec':rec}})
    return render(request, "itemInfo.html", {'oinf': {'inf':inf, 'rec':rec}})
def hostInfo(request, idx):
    fldid = "hid"
    inf = {'fldid':fldid,'itemtype':'Host'}
    lc=0


    rec={}
    lc+=1
    rec['lc']=lc

    rec['i'] = StmtHost.objects.get(id=idx)
    rec['u'] = du.getUsers(fldid,idx)
    rec['q'] = du.getQueries(fldid, idx)
    rec['d'] = du.getDbs(fldid,idx)
    rec['x'] = du.getPrograms(fldid,idx)
    #rec['h'] = du.getHosts(fldid,idx)


    rec['xset1'], rec['yset1'], rec['days1'], rec['fromDt1'] = du.getDataSets(fldid, idx, 500)
    rec['xset2'], rec['yset2'], rec['days2'], rec['fromDt2'] = du.getDataSets(fldid, idx, 30)
    rec['xset3'], rec['yset3'], rec['days3'], rec['fromDt3'] = du.getDataSets(fldid,idx,7)

    rec['xset_hr'],rec['yset_hr']=du.getStmtAvrDrtByHour(fldid,idx)
    rec['xset_di_w'],rec['yset_di_w']= du.getStmtAvrDrtBy(fldid,idx,'calendardayinweek')
    rec['xset_di_m'], rec['yset_di_m'] = du.getStmtAvrDrtBy(fldid,idx, 'calendardayinmonth')

    return render(request, "itemInfo.html", {'oinf': {'inf':inf, 'rec':rec}})
def prgmInfo(request, idx):
    fldid = "xid"
    inf = {'fldid':fldid,'itemtype':'Program'}

    lc=0


    rec={}
    lc+=1
    rec['lc']=lc

    rec['i'] = StmtPrgm.objects.get(id=idx)
    rec['u'] = du.getUsers(fldid,idx)
    rec['q'] = du.getQueries(fldid, idx)
    rec['d'] = du.getDbs(fldid,idx)
    #rec['x'] = du.getPrograms('uid',idx)
    rec['h'] = du.getHosts(fldid,idx)


    rec['xset1'], rec['yset1'], rec['days1'], rec['fromDt1'] = du.getDataSets(fldid, idx, 500)
    rec['xset2'], rec['yset2'], rec['days2'], rec['fromDt2'] = du.getDataSets(fldid, idx, 30)
    rec['xset3'], rec['yset3'], rec['days3'], rec['fromDt3'] = du.getDataSets(fldid,idx,7)

    rec['xset_hr'],rec['yset_hr']=du.getStmtAvrDrtByHour(fldid,idx)
    rec['xset_di_w'],rec['yset_di_w']= du.getStmtAvrDrtBy(fldid,idx,'calendardayinweek')
    rec['xset_di_m'], rec['yset_di_m'] = du.getStmtAvrDrtBy(fldid,idx, 'calendardayinmonth')

    return render(request, "itemInfo.html", {'oinf': {'inf':inf, 'rec':rec}})
def qryInfo(request, qidx):
    qry = StmtQry.objects.get(id=qidx)

    lc=0


    rec={}
    lc+=1
    rec['lc']=lc
    rec['drt'] = qidx
    rec['qexmpl']=du.getQryExpl(qidx)
    rec['q'] = StmtQry.objects.get(id=qidx)
    rec['u'] = du.getUsers('qid',qidx)
    rec['d'] = du.getDbs('qid',qidx)
    rec['x'] = du.getPrograms('qid',qidx)
    rec['h'] = du.getHosts('qid',qidx)

    rec['xset1'], rec['yset1'], rec['days1'], rec['fromDt1'] = du.getDataSets("qid",qidx, 500)
    rec['xset2'], rec['yset2'], rec['days2'], rec['fromDt2'] = du.getDataSets("qid",qidx, 30)
    rec['xset3'], rec['yset3'], rec['days3'], rec['fromDt3'] = du.getDataSets("qid",qidx,7)

    rec['xset_hr'],rec['yset_hr']=du.getStmtAvrDrtByHour("qid",qidx)
    rec['xset_di_w'],rec['yset_di_w']= du.getStmtAvrDrtBy('qid',qidx,'calendardayinweek')
    rec['xset_di_m'], rec['yset_di_m'] = du.getStmtAvrDrtBy('qid',qidx, 'calendardayinmonth')

    return render(request, "qryinfo.html", {'oinf': { 'qry':qry, 'rec':rec }} )