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

import random


usuarios = ['usuario1', 'usuario2', 'usuario3', 'usuario4', 'usuario5']


Vendedores = []


for _ in range(150):

    usuario = random.choice(usuarios)
    

    if Vendedores.count(usuario) < 3:  
        cantidad = random.randint(31, 50)  
    else:
        cantidad = random.randint(1, 29)  
    
    Vendedores.append((usuario, 'articulo', cantidad))

# Vendedores = [('usuario3','articulo',100),
#               ('usuario3','articulo',100),
#               ('usuario3','articulo',100),
#               ('usuario3','articulo',100)]

class VistaSimularVentas(Resource):

    def post(self):
        for vendedor in Vendedores:
            obtener_token = requests.get('http://ec2-52-207-65-64.compute-1.amazonaws.com/autorizar', headers={'usuario':vendedor[0]})
            if obtener_token.status_code == HTTPStatus.UNAUTHORIZED:
                print("Este usuario ya no tiene permisos")
                continue
            payload = {"articulo":vendedor[1],
                       "unidades":vendedor[2]}
            headers = {'Authorization':f'Bearer {json.loads(obtener_token.content)["access_token"]}'}
            procesar_venta = requests.post('http://ec2-3-91-68-22.compute-1.amazonaws.com/crear_venta', json=payload, headers=headers)
            print(procesar_venta.content)
        return {"mensaje": "Experimento finalizado"}
    
api.add_resource(VistaSimularVentas, '/experimento')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6003)









