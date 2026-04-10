from cria_banco import Base, session, queryFromDb
from sqlalchemy import Column, String, Integer

class Schema:
    def toJson(self):
        columns = self.__table__.columns
        result = {}
        
        for column in columns:
            value = getattr(self, column.name)
            result[column.name] = value
        
        return result

class UserModel(Base, Schema):
    __tablename__ = 'usuario'
    
    user_id = Column(Integer, primary_key=True)
    login = Column(String(40), nullable = False)
    senha = Column(String(20), nullable = False) 
     
    def __init__(self, login, senha):
        self.login = login
        self.senha = senha
        
    @classmethod
    def find_user(cls, user_id):
        user = queryFromDb(session.query(cls).filter_by(user_id = user_id).first())
        
        if user:
            return user
        return None
    
    @classmethod
    def find_user_login(cls, login):
        user = queryFromDb(session.query(cls).filter_by(login = login).first())
        
        if user:
            return user
        return None
    
    def save_user(self):
        queryFromDb(session.add(self))  
        
    def delete_user(self):
        queryFromDb(session.delete(self))
        
        
        