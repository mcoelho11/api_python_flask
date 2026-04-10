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
    
    site_id = Column(Integer, primary_key=True)
    url = Column(String(80))
    
    def __init__(self, url):
        self.url = url
        
    @classmethod
    def find_site(cls, url):
        site = queryFromDb(session.query(cls).filter_by(url=url).first())
        
        if site:
           return site
        return None 