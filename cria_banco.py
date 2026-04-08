from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

db_uri = "firebird+firebird://sysdba:masterkey@/C:/Users/Suporte Gplus/Downloads/rest_api_python_flask/HOTEIS.FDB?charset=win1252"
engine = create_engine(db_uri)

Session = sessionmaker(engine, autoflush=False)
session = Session()

Base = declarative_base()
Base.metadata.create_all(engine)

create_table = "\
    CREATE TABLE IF NOT EXISTS Hotel(\
        id_hotel text PRIMARY KEY NOT NULL,\
        nome VARCHAR(150) NOT NULL,\
        estrelas REAL,\
        diaria REAL)"
        
insert_hotel = "INSERT INTO Hotel VALUES('brabo', 'Corinthians Paulista', 5.0, 2000.0)"