from typing import List, Optional

from sqlalchemy import BigInteger, CHAR, Date, DateTime, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, Sequence, SmallInteger, String, Text, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class StmtDb(Base):
    __tablename__ = 'stmt_db'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='stmt_db_pk'),
        Index('stmt_db_pnm_idx', 'pnm'),
        {'schema': 'stmt'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pnm: Mapped[str] = mapped_column(String(255))

    stmt_fact: Mapped[List['StmtFact']] = relationship('StmtFact', back_populates='stmt_db')


class StmtField(Base):
    __tablename__ = 'stmt_field'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='stmt_fields_pk'),
        {'schema': 'stmt'}
    )

    id: Mapped[int] = mapped_column(Integer, Sequence('stmt_fields_id_seq', schema='stmt'), primary_key=True)
    colnm: Mapped[Optional[str]] = mapped_column(String(255))
    tid: Mapped[Optional[int]] = mapped_column(Integer)


class StmtHost(Base):
    __tablename__ = 'stmt_host'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='stmt_host_pk'),
        {'schema': 'stmt'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hnm: Mapped[Optional[str]] = mapped_column(String(255))

    stmt_fact: Mapped[List['StmtFact']] = relationship('StmtFact', back_populates='stmt_host')


class StmtIndata(Base):
    __tablename__ = 'stmt_indata'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='stmt_indata_pk'),
        {'schema': 'stmt'}
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    tm: Mapped[str] = mapped_column(CHAR(4))
    nstmt: Mapped[Optional[str]] = mapped_column(String(255))
    dt: Mapped[Optional[datetime.date]] = mapped_column(Date)
    unm: Mapped[Optional[str]] = mapped_column(String(255), comment='user name')
    dnm: Mapped[Optional[str]] = mapped_column(String(255), comment='database name')
    hnm: Mapped[Optional[str]] = mapped_column(String(255), comment='hostname')
    pnm: Mapped[Optional[str]] = mapped_column(String(255), comment='program name')
    session: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))


class StmtPrgm(Base):
    __tablename__ = 'stmt_prgm'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='stmt_prgm_pk'),
        Index('stmt_prgm_pnm_idx', 'pnm'),
        {'schema': 'stmt'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pnm: Mapped[Optional[str]] = mapped_column(String(255))

    stmt_fact: Mapped[List['StmtFact']] = relationship('StmtFact', back_populates='stmt_prgm')


class StmtQry(Base):
    __tablename__ = 'stmt_qry'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='stmt_qry_pk'),
        {'schema': 'stmt'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nsql: Mapped[str] = mapped_column(String(255))
    name: Mapped[Optional[str]] = mapped_column(String(255))
    nfull: Mapped[Optional[str]] = mapped_column(Text)

    stmt_fact: Mapped[List['StmtFact']] = relationship('StmtFact', back_populates='stmt_qry')
    stmt_qry_exmpl: Mapped[List['StmtQryExmpl']] = relationship('StmtQryExmpl', back_populates='stmt_qry')
    stmt_qry_tab: Mapped[List['StmtQryTab']] = relationship('StmtQryTab', back_populates='stmt_qry')


class StmtTab(Base):
    __tablename__ = 'stmt_tab'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='stmt_tab_pk'),
        {'schema': 'stmt'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tabnm: Mapped[Optional[str]] = mapped_column(String)
    tabinfo: Mapped[Optional[str]] = mapped_column(Text)

    stmt_qry_tab: Mapped[List['StmtQryTab']] = relationship('StmtQryTab', back_populates='stmt_tab')


class StmtUser(Base):
    __tablename__ = 'stmt_user'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='stmt_user_pk'),
        Index('stmt_user_unm_idx', 'unm'),
        {'schema': 'stmt'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unm: Mapped[Optional[str]] = mapped_column(String(255))

    stmt_fact: Mapped[List['StmtFact']] = relationship('StmtFact', back_populates='stmt_user')


class StmtFact(Base):
    __tablename__ = 'stmt_fact'
    __table_args__ = (
        ForeignKeyConstraint(['did'], ['stmt.stmt_db.id'], name='stmt_fact_stmt_db_fk'),
        ForeignKeyConstraint(['hid'], ['stmt.stmt_host.id'], name='stmt_fact_stmt_host_fk'),
        ForeignKeyConstraint(['qid'], ['stmt.stmt_qry.id'], name='stmt_fact_stmt_qry_fk'),
        ForeignKeyConstraint(['uid'], ['stmt.stmt_user.id'], name='stmt_fact_stmt_user_fk'),
        ForeignKeyConstraint(['xid'], ['stmt.stmt_prgm.id'], name='stmt_fact_stmt_prgm_fk'),
        PrimaryKeyConstraint('id', name='stmt_fact_pk'),
        {'schema': 'stmt'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    qid: Mapped[Optional[int]] = mapped_column(Integer)
    dt: Mapped[Optional[datetime.date]] = mapped_column(Date)
    hr: Mapped[Optional[int]] = mapped_column(SmallInteger)
    uid: Mapped[Optional[int]] = mapped_column(Integer)
    did: Mapped[Optional[int]] = mapped_column(Integer)
    hid: Mapped[Optional[int]] = mapped_column(Integer)
    xid: Mapped[Optional[int]] = mapped_column(Integer)
    cnt: Mapped[Optional[int]] = mapped_column(Integer)

    stmt_db: Mapped[Optional['StmtDb']] = relationship('StmtDb', back_populates='stmt_fact')
    stmt_host: Mapped[Optional['StmtHost']] = relationship('StmtHost', back_populates='stmt_fact')
    stmt_qry: Mapped[Optional['StmtQry']] = relationship('StmtQry', back_populates='stmt_fact')
    stmt_user: Mapped[Optional['StmtUser']] = relationship('StmtUser', back_populates='stmt_fact')
    stmt_prgm: Mapped[Optional['StmtPrgm']] = relationship('StmtPrgm', back_populates='stmt_fact')


class StmtQryExmpl(Base):
    __tablename__ = 'stmt_qry_exmpl'
    __table_args__ = (
        ForeignKeyConstraint(['qid'], ['stmt.stmt_qry.id'], name='stmt_qry_txt_stmt_qry_fk'),
        PrimaryKeyConstraint('id', name='stmt_qry_txt_pk'),
        {'schema': 'stmt'}
    )

    id: Mapped[int] = mapped_column(Integer, Sequence('stmt_qry_txt_id_seq', schema='stmt'), primary_key=True)
    dttm: Mapped[datetime.datetime] = mapped_column(DateTime)
    qid: Mapped[Optional[int]] = mapped_column(Integer)
    stxt: Mapped[Optional[str]] = mapped_column(Text)

    stmt_qry: Mapped[Optional['StmtQry']] = relationship('StmtQry', back_populates='stmt_qry_exmpl')


class StmtQryTab(Base):
    __tablename__ = 'stmt_qry_tab'
    __table_args__ = (
        ForeignKeyConstraint(['qid'], ['stmt.stmt_qry.id'], name='stmt_qry_tab_stmt_qry_fk'),
        ForeignKeyConstraint(['tabid'], ['stmt.stmt_tab.id'], name='stmt_qry_tab_stmt_tab_fk'),
        PrimaryKeyConstraint('id', name='stmt_qry_tabs_pk'),
        {'schema': 'stmt'}
    )

    id: Mapped[int] = mapped_column(Integer, Sequence('stmt_qry_tabs_id_seq', schema='stmt'), primary_key=True)
    tabid: Mapped[Optional[int]] = mapped_column(Integer)
    qid: Mapped[Optional[int]] = mapped_column(Integer)

    stmt_qry: Mapped[Optional['StmtQry']] = relationship('StmtQry', back_populates='stmt_qry_tab')
    stmt_tab: Mapped[Optional['StmtTab']] = relationship('StmtTab', back_populates='stmt_qry_tab')
