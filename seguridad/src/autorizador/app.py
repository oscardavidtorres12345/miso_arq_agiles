import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api

from flask import jsonify
from flask_jwt_extended import create_access_token, JWTManager

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

class IdentidadPersona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(15))
    permitido = db.Column(db.Boolean, default=True)
    
with app.app_context():
    db.create_all()

    if not IdentidadPersona.query.first():
        usuarios_iniciales = [
            IdentidadPersona(usuario="usuario1"),
            IdentidadPersona(usuario="usuario2"),
            IdentidadPersona(usuario="usuario3"),
            IdentidadPersona(usuario="usuario4"),
            IdentidadPersona(usuario="usuario5")
        ]
        
        db.session.add_all(usuarios_iniciales)
        db.session.commit()

api = Api(app)

class VistaAutorizador(Resource):

    def get(self):
        usuario = request.headers.get('usuario', None)
        persona = IdentidadPersona.query.filter_by(usuario=usuario).first()
        
        if persona and persona.permitido == True:
            token_acceso = create_access_token(identity=usuario)
            return jsonify(access_token=token_acceso)
          
        return {"mensaje": "Sin autorización, permisos revocados"}, 401

class VistaRevocar(Resource):
    def put(self):
        usuario = request.headers.get('usuario', None)
        persona = IdentidadPersona.query.filter_by(usuario=usuario).first_or_404()
        persona.permitido = False
        db.session.add(persona)
        db.session.commit()
        return {"mensaje": "Revocación de acceso"}, 200

api.add_resource(VistaAutorizador, '/autorizar')
api.add_resource(VistaRevocar, '/revocar')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('SERVICE_PORT', 6001)))
