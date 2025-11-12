import logging
logging.basicConfig( level=logging.DEBUG)
import json
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import os
import dbutils.qryparsing as d


def load_config(path: str  ="./cfg/config.json", section: str = "postgresql") -> dict:
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
    host = cfg.get("host", "localhost")
    port = cfg.get("port", 5432)
    database = cfg["database"]

    return f"{dialect}+{driver}://{user}:{password}@{host}:{port}/{database}"


def main():

    print(Path.cwd())
    print(os.environ)
    print("-------------------")

    config = load_config()
    db_url = build_connection_url(config)
    try:
        engine = create_engine(db_url)

        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.scalar()
            print("Connection  OK →", version)

    except SQLAlchemyError as e:
        print("❌ ERROR SQLAlchemy:", e)

    d.parsingNewRecordsDictionary(engine)
    d.parsingNewRecordsHistory(engine,{'setstatus':1,'clean':1})
    #d.parsingNewRecordsHistory(engine, { 'clean': 1})
    #rowcnt=d.parsingNewQryExamples(engine,{'setstatus':1})
    #print (rowcnt)
if __name__ == "__main__":
    main()