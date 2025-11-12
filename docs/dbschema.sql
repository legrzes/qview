-- DROP SCHEMA stmt;

CREATE SCHEMA stmt AUTHORIZATION pgadmin;

-- DROP SEQUENCE stmt.dim_calendar_id_seq;

CREATE SEQUENCE stmt.dim_calendar_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE stmt.stmt_db_id_seq;

CREATE SEQUENCE stmt.stmt_db_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE stmt.stmt_fact_id_seq;

CREATE SEQUENCE stmt.stmt_fact_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE stmt.stmt_fields_id_seq;

CREATE SEQUENCE stmt.stmt_fields_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE stmt.stmt_host_id_seq;

CREATE SEQUENCE stmt.stmt_host_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE stmt.stmt_indata_id_seq;

CREATE SEQUENCE stmt.stmt_indata_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE stmt.stmt_inexmpl_id_seq;

CREATE SEQUENCE stmt.stmt_inexmpl_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE stmt.stmt_prgm_id_seq;

CREATE SEQUENCE stmt.stmt_prgm_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE stmt.stmt_qry_id_seq;

CREATE SEQUENCE stmt.stmt_qry_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE stmt.stmt_qry_tabs_id_seq;

CREATE SEQUENCE stmt.stmt_qry_tabs_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE stmt.stmt_qry_txt_id_seq;

CREATE SEQUENCE stmt.stmt_qry_txt_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE stmt.stmt_srv_id_seq;

CREATE SEQUENCE stmt.stmt_srv_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE stmt.stmt_tab_id_seq;

CREATE SEQUENCE stmt.stmt_tab_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE stmt.stmt_user_id_seq;

CREATE SEQUENCE stmt.stmt_user_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;-- stmt.dim_calendar definition

-- Drop table

-- DROP TABLE stmt.dim_calendar;

CREATE TABLE stmt.dim_calendar (
	id serial4 NOT NULL,
	dt date NOT NULL,
	dateshortdescription varchar(50) NULL,
	dayshortname varchar(10) NULL,
	monthshortname varchar(10) NULL,
	calendarday int2 NULL,
	calendarweek int2 NULL,
	calendarweekstartdateid int4 NULL,
	calendarweekenddateid int4 NULL,
	calendardayinweek int2 NULL,
	calendarmonth int2 NULL,
	calendarmonthstartdateid int4 NULL,
	calendarmonthenddateid int4 NULL,
	calendarnumberofdaysinmonth int2 NULL,
	calendardayinmonth int2 NULL,
	calendarquarter int2 NULL,
	calendarquarterstartdateid int4 NULL,
	calendarquarterenddateid int4 NULL,
	calendarnumberofdaysinquarter int2 NULL,
	calendardayinquarter int2 NULL,
	calendaryear int2 NULL,
	CONSTRAINT dim_calendar_pk PRIMARY KEY (id)
);


-- stmt.stmt_db definition

-- Drop table

-- DROP TABLE stmt.stmt_db;

CREATE TABLE stmt.stmt_db (
	id serial4 NOT NULL,
	dnm varchar(255) NOT NULL,
	CONSTRAINT stmt_db_pk PRIMARY KEY (id)
);
CREATE INDEX stmt_db_pnm_idx ON stmt.stmt_db USING btree (dnm);


-- stmt.stmt_field definition

-- Drop table

-- DROP TABLE stmt.stmt_field;

CREATE TABLE stmt.stmt_field (
	id int4 DEFAULT nextval('stmt.stmt_fields_id_seq'::regclass) NOT NULL,
	colnm varchar(255) NULL,
	tid int4 NULL,
	CONSTRAINT stmt_fields_pk PRIMARY KEY (id)
);


-- stmt.stmt_host definition

-- Drop table

-- DROP TABLE stmt.stmt_host;

CREATE TABLE stmt.stmt_host (
	id serial4 NOT NULL,
	hnm varchar(255) NULL,
	CONSTRAINT stmt_host_pk PRIMARY KEY (id)
);


-- stmt.stmt_indata definition

-- Drop table

-- DROP TABLE stmt.stmt_indata;

CREATE TABLE stmt.stmt_indata (
	id bigserial NOT NULL,
	nqry varchar(255) DEFAULT '-'::character varying NULL,
	dt date NULL,
	tm bpchar(4) NOT NULL,
	unm varchar(255) DEFAULT '-'::character varying NULL, -- user name
	dnm varchar(255) DEFAULT '-'::character varying NULL, -- database name
	hnm varchar(255) DEFAULT '-'::character varying NULL, -- hostname
	xnm varchar(255) DEFAULT '-'::character varying NULL, -- program name
	sesnum int4 NULL,
	status int4 DEFAULT 0 NULL,
	"server" varchar NULL,
	CONSTRAINT stmt_indata_pk PRIMARY KEY (id)
);

-- Column comments

COMMENT ON COLUMN stmt.stmt_indata.unm IS 'user name';
COMMENT ON COLUMN stmt.stmt_indata.dnm IS 'database name';
COMMENT ON COLUMN stmt.stmt_indata.hnm IS 'hostname';
COMMENT ON COLUMN stmt.stmt_indata.xnm IS 'program name';


-- stmt.stmt_inexmpl definition

-- Drop table

-- DROP TABLE stmt.stmt_inexmpl;

CREATE TABLE stmt.stmt_inexmpl (
	id serial4 NOT NULL,
	nqry varchar(255) DEFAULT '-'::character varying NULL,
	fqry text DEFAULT '-'::text NULL,
	dt date NULL,
	status int2 DEFAULT 0 NOT NULL,
	CONSTRAINT stmt_inexmpl_pk PRIMARY KEY (id)
);


-- stmt.stmt_prgm definition

-- Drop table

-- DROP TABLE stmt.stmt_prgm;

CREATE TABLE stmt.stmt_prgm (
	id serial4 NOT NULL,
	xnm varchar(255) NULL,
	CONSTRAINT stmt_prgm_pk PRIMARY KEY (id)
);
CREATE INDEX stmt_prgm_pnm_idx ON stmt.stmt_prgm USING btree (xnm);


-- stmt.stmt_qry definition

-- Drop table

-- DROP TABLE stmt.stmt_qry;

CREATE TABLE stmt.stmt_qry (
	id serial4 NOT NULL,
	nqry varchar(255) NOT NULL,
	"name" varchar(255) NULL,
	nfull text NULL,
	CONSTRAINT stmt_qry_pk PRIMARY KEY (id)
);


-- stmt.stmt_srv definition

-- Drop table

-- DROP TABLE stmt.stmt_srv;

CREATE TABLE stmt.stmt_srv (
	id serial4 NOT NULL,
	snm varchar NULL,
	CONSTRAINT stmt_srv_pk PRIMARY KEY (id)
);


-- stmt.stmt_tab definition

-- Drop table

-- DROP TABLE stmt.stmt_tab;

CREATE TABLE stmt.stmt_tab (
	id serial4 NOT NULL,
	tabnm varchar NULL,
	tabinfo text NULL,
	CONSTRAINT stmt_tab_pk PRIMARY KEY (id)
);


-- stmt.stmt_user definition

-- Drop table

-- DROP TABLE stmt.stmt_user;

CREATE TABLE stmt.stmt_user (
	id serial4 NOT NULL,
	unm varchar(255) NULL,
	CONSTRAINT stmt_user_pk PRIMARY KEY (id)
);
CREATE INDEX stmt_user_unm_idx ON stmt.stmt_user USING btree (unm);


-- stmt.stmt_fact definition

-- Drop table

-- DROP TABLE stmt.stmt_fact;

CREATE TABLE stmt.stmt_fact (
	id serial4 NOT NULL,
	qid int4 NULL,
	dt date NULL,
	hr int2 NULL,
	uid int4 NULL,
	did int4 NULL,
	hid int4 NULL,
	xid int4 NULL,
	cnt int4 NULL,
	sid int4 NULL,
	CONSTRAINT stmt_fact_pk PRIMARY KEY (id),
	CONSTRAINT stmt_fact_stmt_db_fk FOREIGN KEY (did) REFERENCES stmt.stmt_db(id),
	CONSTRAINT stmt_fact_stmt_host_fk FOREIGN KEY (hid) REFERENCES stmt.stmt_host(id),
	CONSTRAINT stmt_fact_stmt_prgm_fk FOREIGN KEY (xid) REFERENCES stmt.stmt_prgm(id),
	CONSTRAINT stmt_fact_stmt_qry_fk FOREIGN KEY (qid) REFERENCES stmt.stmt_qry(id),
	CONSTRAINT stmt_fact_stmt_srv_fk FOREIGN KEY (sid) REFERENCES stmt.stmt_srv(id),
	CONSTRAINT stmt_fact_stmt_user_fk FOREIGN KEY (uid) REFERENCES stmt.stmt_user(id)
);
CREATE UNIQUE INDEX stmt_fact_qid_idx ON stmt.stmt_fact USING btree (qid, dt, hr, uid, did, hid, xid, sid);


-- stmt.stmt_qry_exmpl definition

-- Drop table

-- DROP TABLE stmt.stmt_qry_exmpl;

CREATE TABLE stmt.stmt_qry_exmpl (
	id int4 DEFAULT nextval('stmt.stmt_qry_txt_id_seq'::regclass) NOT NULL,
	qid int4 NULL,
	dttm timestamp NOT NULL,
	stxt text NULL,
	CONSTRAINT stmt_qry_txt_pk PRIMARY KEY (id),
	CONSTRAINT stmt_qry_txt_stmt_qry_fk FOREIGN KEY (qid) REFERENCES stmt.stmt_qry(id)
);
CREATE INDEX stmt_qry_exmpl_qid_idx ON stmt.stmt_qry_exmpl USING btree (qid, dttm);


-- stmt.stmt_qry_tab definition

-- Drop table

-- DROP TABLE stmt.stmt_qry_tab;

CREATE TABLE stmt.stmt_qry_tab (
	id int4 DEFAULT nextval('stmt.stmt_qry_tabs_id_seq'::regclass) NOT NULL,
	tabid int4 NULL,
	qid int4 NULL,
	CONSTRAINT stmt_qry_tabs_pk PRIMARY KEY (id),
	CONSTRAINT stmt_qry_tab_stmt_qry_fk FOREIGN KEY (qid) REFERENCES stmt.stmt_qry(id),
	CONSTRAINT stmt_qry_tab_stmt_tab_fk FOREIGN KEY (tabid) REFERENCES stmt.stmt_tab(id)
);


-- stmt.vm_stmt_fact_avg30 source

CREATE MATERIALIZED VIEW stmt.vm_stmt_fact_avg30
TABLESPACE pg_default
AS SELECT qid,
    uid,
    did,
    hid,
    xid,
    sum(cnt) AS cnt
   FROM stmt.stmt_fact
  WHERE dt >= (CURRENT_DATE - '30 days'::interval)
  GROUP BY qid, uid, did, hid, xid
WITH DATA;


-- stmt.vm_stmt_fact_avg7 source

CREATE MATERIALIZED VIEW stmt.vm_stmt_fact_avg7
TABLESPACE pg_default
AS SELECT qid,
    uid,
    did,
    hid,
    xid,
    sum(cnt) AS cnt
   FROM stmt.stmt_fact
  WHERE dt >= (CURRENT_DATE - '7 days'::interval)
  GROUP BY qid, uid, did, hid, xid
WITH DATA;


-- stmt.vm_stmt_fact_avgday source

CREATE MATERIALIZED VIEW stmt.vm_stmt_fact_avgday
TABLESPACE pg_default
AS SELECT qid,
    dt,
    uid,
    did,
    hid,
    xid,
    sum(cnt) AS cnt
   FROM stmt.stmt_fact
  GROUP BY qid, dt, uid, did, hid, xid
WITH DATA;


-- stmt.vm_stmt_fact_avghr source

CREATE MATERIALIZED VIEW stmt.vm_stmt_fact_avghr
TABLESPACE pg_default
AS SELECT qid,
    hr,
    uid,
    did,
    hid,
    xid,
    sum(cnt) AS cnt
   FROM stmt.stmt_fact
  GROUP BY qid, hr, uid, did, hid, xid
WITH DATA;