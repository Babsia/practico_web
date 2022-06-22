from __main__ import app
from flask_sqlalchemy import SQLAlchemy
from datetime import date 

db = SQLAlchemy(app)

class usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer,primary_key = True)
    nombre =db.Column(db.String(80),nullable = False)
    correo = db.Column(db.String(120),unique = True, nullable = False)
    clave =db.Column(db.String(120),nullable = False)
    receta = db.relationship('receta',backref ='usuario',cascade = 'all, delete-orphan')
    

class receta(db.Model):
    __tablename__ = "receta"
    id = db.Column(db.Integer,primary_key = True)
    nombre = db.Column(db.String(100),nullable = False)
    tiempo = db.Column(db.Integer,nullable = False)
    elaboracion = db.Column(db.String(100),nullable = False)
    cantidadmegusta = db.Column(db.Integer,nullable = False)
    fecha = db.Column(db.Date,nullable = False)
    usuarioid = db.Column(db.Integer,db.ForeignKey('usuario.id'))
    ingrediente = db.relationship('ingrediente',backref ='receta',cascade = 'all, delete-orphan')

class ingrediente(db.Model):
    __tablename__ = "ingrediente"
    id = db.Column(db.Integer,primary_key = True)
    nombre = db.Column(db.String(80),nullable = False)
    cantidad = db.Column(db.Integer,nullable = False)
    unidad = db.Column(db.Integer,nullable = False)
    recetaID = db.Column(db.Integer,db.ForeignKey('receta.id'))