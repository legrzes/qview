from django.db import models

# Create your models here.

class StmtDb(models.Model):
    dnm = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'stmt_db'


class StmtFact(models.Model):
    qid = models.ForeignKey('StmtQry', models.DO_NOTHING, db_column='qid', blank=True, null=True)
    dt = models.DateField(blank=True, null=True)
    hr = models.SmallIntegerField(blank=True, null=True)
    uid = models.ForeignKey('StmtUser', models.DO_NOTHING, db_column='uid', blank=True, null=True)
    did = models.ForeignKey(StmtDb, models.DO_NOTHING, db_column='did', blank=True, null=True)
    hid = models.ForeignKey('StmtHost', models.DO_NOTHING, db_column='hid', blank=True, null=True)
    xid = models.ForeignKey('StmtPrgm', models.DO_NOTHING, db_column='xid', blank=True, null=True)
    cnt = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "{} {} {}={}".format(self.dt,self.hr,self.qid,self.cnt)
    class Meta:
        managed = False
        db_table = 'stmt_fact'
        unique_together = (('qid', 'dt', 'hr', 'uid', 'did', 'hid', 'xid'),)


class StmtField(models.Model):
    def __str__(self):
        return self.colnm
    colnm = models.CharField(max_length=255, blank=True, null=True)
    tid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stmt_field'


class StmtHost(models.Model):
    hnm = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.hnm
    class Meta:
        managed = False
        db_table = 'stmt_host'


class StmtIndata(models.Model):
    id = models.BigAutoField(primary_key=True)
    nqry = models.CharField(max_length=255, blank=True, null=True)
    dt = models.DateField(blank=True, null=True)
    tm = models.CharField(max_length=4)
    unm = models.CharField(max_length=255, blank=True, null=True, db_comment='user name')
    dnm = models.CharField(max_length=255, blank=True, null=True, db_comment='database name')
    hnm = models.CharField(max_length=255, blank=True, null=True, db_comment='hostname')
    xnm = models.CharField(max_length=255, blank=True, null=True, db_comment='program name')
    sesnum = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stmt_indata'


class StmtInexmpl(models.Model):
    nsql = models.CharField(max_length=255, blank=True, null=True)
    fsql = models.TextField(blank=True, null=True)
    dt = models.DateField(blank=True, null=True)
    status = models.SmallIntegerField()
    def __str__(self):
        return self.nsql
    class Meta:
        managed = False
        db_table = 'stmt_inexmpl'


class StmtPrgm(models.Model):
    xnm = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.xnm
    class Meta:
        managed = False
        db_table = 'stmt_prgm'


class StmtQry(models.Model):
    nqry = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    nfull = models.TextField(blank=True, null=True)
    def __str__(self):
        return "{}|{}".format(self.id,self.nqry)
    class Meta:
        managed = False
        db_table = 'stmt_qry'


class StmtQryExmpl(models.Model):
    qid = models.ForeignKey(StmtQry, models.DO_NOTHING, db_column='qid', blank=True, null=True)
    dttm = models.DateTimeField()
    stxt = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stmt_qry_exmpl'


class StmtQryTab(models.Model):
    tabid = models.ForeignKey('StmtTab', models.DO_NOTHING, db_column='tabid', blank=True, null=True)
    qid = models.ForeignKey(StmtQry, models.DO_NOTHING, db_column='qid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stmt_qry_tab'


class StmtTab(models.Model):
    tabnm = models.CharField(blank=True, null=True)
    tabinfo = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.tabnm
    class Meta:
        managed = False
        db_table = 'stmt_tab'


class StmtUser(models.Model):
    unm = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.unm
    class Meta:
        managed = False
        db_table = 'stmt_user'

class DimCalendar(models.Model):
    dt = models.DateField()
    dateshortdescription = models.CharField(max_length=50, blank=True, null=True)
    dayshortname = models.CharField(max_length=10, blank=True, null=True)
    monthshortname = models.CharField(max_length=10, blank=True, null=True)
    calendarday = models.SmallIntegerField(blank=True, null=True)
    calendarweek = models.SmallIntegerField(blank=True, null=True)
    calendarweekstartdateid = models.IntegerField(blank=True, null=True)
    calendarweekenddateid = models.IntegerField(blank=True, null=True)
    calendardayinweek = models.SmallIntegerField(blank=True, null=True)
    calendarmonth = models.SmallIntegerField(blank=True, null=True)
    calendarmonthstartdateid = models.IntegerField(blank=True, null=True)
    calendarmonthenddateid = models.IntegerField(blank=True, null=True)
    calendarnumberofdaysinmonth = models.SmallIntegerField(blank=True, null=True)
    calendardayinmonth = models.SmallIntegerField(blank=True, null=True)
    calendarquarter = models.SmallIntegerField(blank=True, null=True)
    calendarquarterstartdateid = models.IntegerField(blank=True, null=True)
    calendarquarterenddateid = models.IntegerField(blank=True, null=True)
    calendarnumberofdaysinquarter = models.SmallIntegerField(blank=True, null=True)
    calendardayinquarter = models.SmallIntegerField(blank=True, null=True)
    calendaryear = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_calendar'