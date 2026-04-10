from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.user import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLE'] = True
api = Api(app)
jwt  = JWTManager(app)

@jwt.token_in_blocklist_loader
def verifica_blacklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalido(jwt_header, jwt_payload):
    return jsonify({'message': 'You have benn logged out.'})
    
    
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<int:id>')
api.add_resource(User, '/usuario/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    app.run(debug=True)

# http://127.0.0.1:5000/hoteis
