from flask_restful import Resource, reqparse
from models.user_model import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from hmac import compare_digest
from blacklist import BLACKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('login', required=True)
atributos.add_argument('senha', required=True)
  
class User(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('login', required = True)
    argumentos.add_argument('senha', required = True)
    
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        
        if user:
            return user.toJson()
        return { 'message': 'User not found.' }, 404
    
    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            user.delete_user()
            return{ 'message' : 'User deleted.' }
        return { 'message' : 'User not found.' }, 404
    
class UserRegister(Resource):
    def post(self):
        dados = atributos.parse_args()
        
        if UserModel.find_user_login(dados['login']):
            return { "message": "The login '{}' already existis.".format(dados['login']) }
        
        user = UserModel(**dados)
        user.save_user()
        
        return { 'message': 'Login created.' }, 201
    
class UserLogin(Resource):
    def post(self):
        dados = atributos.parse_args()
        
        user = UserModel.find_user_login(dados['login'])
        
        if user and compare_digest(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return { 'access_token': token_de_acesso }, 200
            
        return { 'message': 'The username or password is incorrect.' }, 401
    
class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return { 'message': 'Logged out successfully!' }, 200