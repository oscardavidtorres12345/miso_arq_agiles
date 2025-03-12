from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api

from flask_jwt_extended import JWTManager
import requests

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbapp.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()
jwt = JWTManager(app)

db.init_app(app)

class RegistrarEvento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(15))
    payload = db.Column(db.JSON)
    strike = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

api = Api(app)



class VistaEvento(Resource):

    def post(self):
        usuario = request.headers.get('usuario')
        eventos = RegistrarEvento.query.filter_by(usuario=usuario, strike=True).count()
        if eventos >= 3:
            evento = RegistrarEvento(usuario=usuario, payload={"message": "intento de acceso no autorizado"}, strike=True)
            requests.put('http://127.0.0.1:5000/revocar', headers={'usuario':usuario})
            db.session.add(evento)
            db.session.commit()
            return '', 401
        else:
            payload = {"usuario": usuario,
                        "articulo": request.json["articulo"],
                        "unidades": request.json["unidades"]}
            evento = RegistrarEvento(usuario=usuario, payload=payload, strike=request.json["strike"])
            db.session.add(evento)
            db.session.commit()
            return
api.add_resource(VistaEvento, '/registrar_evento')


if __name__ == '__main__':
    app.run(debug=True, port=7000)









