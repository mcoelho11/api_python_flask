from cria_banco import Base, session, queryFromDb
from sqlalchemy import Column, String, Integer

class Schema():
    def toJson(self):
        columns = self.__table__.columns
        result = {}
        
        for column in columns:
            value = getattr(self, column.name)
            result[column.name] = value
        
        return result

class SiteModel(Base, Schema):
    __tablename__ = 'SITE'
    
    site_id = Column()