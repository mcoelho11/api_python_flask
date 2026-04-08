from flask_restful import Resource, reqparse
from models.hotel_model import HotelModel
from flask import jsonify
from cria_banco import session, Session

hoteis = [
    {
        'id': 'alpha',
        'nome': 'Hotel Alpha',
        'estrelas': 4.5,
        'diaria': 420.34,
    },
    {
        'id': 'bravo',
        'nome': 'Hotel Bravo', 
        'estrelas': 4.0,
        'diaria': 380.90,
    },
    {
        'id': 'charlie',
        'nome': 'Hotel Charlie',
        'estrelas': 3.5,
        'diaria': 320.00,
    }
    
]

class Hoteis(Resource):
    def get(self):
        try:
            Session.begin()
            hoteis = session.query(HotelModel).all()
            session.commit() 
        except Exception as e:
            print(str(e))
            session.rollback() 
            
        response = []
        for hotel in hoteis:
            response.append(hotel.toJson())
        return response

    
class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('name')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')

    def find_hotel(id):
        for hotel in hoteis:
            if hotel['id'] == id:
                return hotel
        return None

    def get(self, id):
        hotel = Hotel.find_hotel(id)
        if hotel: 
            return hotel
        return {'message': 'Hotel not found.'}, 404

    def post(self, id):
        dados = Hotel.argumentos.parse_args()
        hotel_obj = HotelModel(id, **dados)
        novo_hotel = hotel_obj.json()
        hoteis.append(novo_hotel)

        return novo_hotel, 200

    def put(self, id):
        dados = Hotel.argumentos.parse_args()
        hotel_obj = HotelModel(id, **dados)
        novo_hotel = hotel_obj.json()
        hotel = Hotel.find_hotel(id)
        
        if hotel: 
            hotel.update(novo_hotel)
            return novo_hotel, 200
        hoteis.append(novo_hotel)
        return novo_hotel, 201

    def delete(self, id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['id'] != id]
        return {'message': 'Hotel deleted.'}        