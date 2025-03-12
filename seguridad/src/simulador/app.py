from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api


from flask import jsonify
import requests
import json
from http import HTTPStatus

db = SQLAlchemy()

app = Flask(__name__)

app_context = app.app_context()
app_context.push()


api = Api(app)

Vendedores = [('usuario1','articulo',100),
              ('usuario1','articulo',100),
              ('usuario1','articulo',100),
              ('usuario1','articulo',100)]

class VistaSimularVentas(Resource):

    def post(self):
        for vendedor in Vendedores:
            obtener_token = requests.get('http://127.0.0.1:5000/autorizar', headers={'usuario':vendedor[0]})
            if obtener_token.status_code == HTTPStatus.UNAUTHORIZED:
                print("Este usuario ya no tiene permisos")
                continue
            payload = {"articulo":vendedor[1],
                       "unidades":vendedor[2]}
            headers = {'Authorization':f'Bearer {json.loads(obtener_token.content)["access_token"]}'}
            procesar_venta = requests.post('http://127.0.0.1:6000/crear_venta', json=payload, headers=headers)
            print(procesar_venta.content)
        return {"mensaje": "Experimento finalizado"}
    
api.add_resource(VistaSimularVentas, '/experimento')


if __name__ == '__main__':
    app.run(debug=True, port=8000)









