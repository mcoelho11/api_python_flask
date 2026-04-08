from cria_banco import Base
from sqlalchemy import Column, String, Float, Integer

class Schema:
    def toJson(self):
        columns = self.__table__.columns
        result = {}
        
        for column in columns:
            value = getattr(self, column.name)
            result[column.name] = value
        
        return result

class HotelModel(Base, Schema):
    __tablename__ = 'HOTEL'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(80), nullable = False)
    estrelas = Column(Float(precision = 1), nullable = False)
    diaria = Column(Float(precision = 2), nullable = False)
    
     
    def __init__(self, id, nome, estrelas, diaria):
        self.id = id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria


