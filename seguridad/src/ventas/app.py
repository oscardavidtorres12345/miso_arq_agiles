from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api

from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from http import HTTPStatus
import requests


db = SQLAlchemy()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()
jwt = JWTManager(app)

api = Api(app)


class VistaVenta(Resource):

    @jwt_required()
    def post(self):
        usuario_actual = get_jwt_identity()
        articulo = request.json["articulo"]
        unidades = request.json["unidades"]
        payload = {"articulo": articulo, "unidades": unidades, "strike": False}
        headers = {'usuario':usuario_actual}
        if unidades > 30:
            payload['strike'] = True
        response = requests.post('http://127.0.0.1:7000/registrar_evento',json=payload, headers=headers) 
        if response.status_code != HTTPStatus.UNAUTHORIZED:
            return {"mensaje": "Venta registrada exitosamente"}, 200
        return {"mensaje": "El usuario no tiene permisos para realizar la solicitud"}, 401

api.add_resource(VistaVenta, '/crear_venta')


if __name__ == '__main__':
    app.run(debug=True, port=6000)









