from flask_restful import Resource, reqparse
from models.hotel_model import HotelModel
from flask_jwt_extended import jwt_required
from cria_banco import session

path_params = reqparse.RequestParser()
path_params.add_argument('nome', type=str, location='args')
path_params.add_argument('estrelas_min', type=float, location='args')
path_params.add_argument('estrelas_max', type=float, location='args')
path_params.add_argument('diaria_min', type=float, location='args')
path_params.add_argument('diaria_max', type=float, location='args')

def normalize_path_params(nome = None, estrelas_min=0, estrelas_max = 5, diaria_min = 0, diaria_max = 10000, **dados):
    return {
            'nome': nome,
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
        }


class Hoteis(Resource):
    def get(self):
        dados = path_params.parse_args()
        dados_validos = { chave:dados[chave] for chave in dados if dados[chave] is not None }
        filters = normalize_path_params(**dados_validos)
        
        if not filters.get('nome'):
            query = session.query(HotelModel).filter(
                HotelModel.estrelas >= filters.get('estrelas_min'),
                HotelModel.estrelas <= filters.get('estrelas_max'),
                HotelModel.diaria >= filters.get('diaria_min'),
                HotelModel.diaria <= filters.get('diaria_max')
            )
        else:
            query = session.query(HotelModel).filter(
                HotelModel.nome == filters.get('nome'),
                HotelModel.estrelas >= filters.get('estrelas_min'),
                HotelModel.estrelas <= filters.get('estrelas_max'),
                HotelModel.diaria >= filters.get('diaria_min'),
                HotelModel.diaria <= filters.get('diaria_max')
            )
        
        hoteis = query.all()
            
        response = []
        for hotel in hoteis:
            response.append(hotel.toJson())
        return response
    
class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', required = True)
    argumentos.add_argument('estrelas', required = True)
    argumentos.add_argument('diaria')
    
    def get(self, id):
        hotel = HotelModel.find_hotel(id)
        
        if hotel:
            return hotel.toJson()
        return { 'Message': 'Hotel not found.' }, 404
    
    @jwt_required()
    def post(self, id):
        if HotelModel.find_hotel(id):
            return {"message": "Hotel id '{}' already exists.".format(id)}, 400
                
        dados = Hotel.argumentos.parse_args()
        hotel_obj = HotelModel(id, **dados)
        hotel_obj.save_hotel()
        
        return hotel_obj.toJson()
    
    @jwt_required()
    def put(self, id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(id)
        
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.toJson(), 200
        
        return { "Message": "Hotel not found. Use POST to create a new hotel." }
    
    @jwt_required()
    def delete(self, id):
        hotel = HotelModel.find_hotel(id)
        if hotel:
            hotel.delete_hotel()
            return{ "Message" : "Hotel deleted." }
        return { "Message" : "Hotel not found." }, 404