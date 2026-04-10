from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

db_uri = "firebird+firebird://sysdba:masterkey@/C:/Users/Suporte Gplus/Downloads/rest_api_python_flask/HOTEIS.FDB?charset=win1252"
engine = create_engine(db_uri)

Session = sessionmaker(engine, autoflush=False, expire_on_commit=False)
session = Session()

def queryFromDb(expression):
    try:
        Session.begin()
        res = expression
        session.commit()
        return res
    except:
        session.rollback

Base = declarative_base()
Base.metadata.create_all(engine)