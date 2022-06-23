
from datetime import datetime
from re import template
from venv import create
from flask import Flask, redirect
from flask import render_template
from flask import request,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import false
from werkzeug.security import generate_password_hash,check_password_hash
import hashlib
from almacenamiento import usuarioprueba,recetaprueba
from datetime import date

sesion=usuarioprueba()
app=Flask(__name__)
app.config.from_pyfile("config.py")
mg='no'
id1=recetaprueba()

from models import db
from models import usuario,receta,ingrediente

@app.route('/')
def login():
    sesion.delusuario()
    return render_template('Log-in.html')


@app.route('/inicio',methods=['GET','POST'])
def checklogin():#Hecha   
    password=request.form['passwrd']
    password2=hashlib.md5(bytes(password,encoding='utf-8')).hexdigest()
    
    user = usuario.query.filter_by(correo = request.form['mail']).first()
    sesion.addusuario(user)
    if user is not None:
        if user.clave==password2:
            return render_template('NavBar.html', Nombre=(sesion.unusuario.nombre))
        else:
            return render_template('Error.html', error = 'Password invalid')
    else:
        return render_template('Error.html', error = 'User invalid')
@app.route('/pagina_principal',methods=['GET','POST'])
def pagina_principal():
    return render_template('NavBar.html', Nombre=(sesion.unusuario.nombre))


#Ingresar Receta atraves de NavBar
@app.route('/IngresarReceta',methods=['GET','POST'])
def ingresarReceta():
    return render_template('ingresar.html', Nombre=(sesion.unusuario.nombre))

@app.route('/recetaingresada',methods=['POST'])#ingresar una receta y guardarla en la base de datos
def recetaingresada(): 

    nombre=request.form['nombre'].capitalize()
    tiempo=request.form['tiempo']
    elaboracion=request.form['elaboracion'].capitalize()
    megusta=0
    ingredientes = 0
    fecha=date.today()
    userID=sesion.unusuario.id
    receta1=receta(nombre=nombre,tiempo=int(tiempo),elaboracion=elaboracion,cantidadmegusta=megusta,fecha=fecha,usuarioid=userID)
    db.session.add(receta1)
    db.session.commit()

    return render_template('ingredientes.html', Nombre=(sesion.unusuario.nombre),idreceta=receta1.id,ingredientes = ingredientes,mensaje ='Ingrese ingrediente')


@app.route('/agregarIngrediente',methods=['GET','POST'])
def agregarOtroIngrediente():#Hecha
    nroI = int(request.form['ingredientes'])
    if(request.form['nombre'] and request.form['Cantidad'] and request.form['unidad'] and nroI != 10):
        ingredienteNuevo = ingrediente(nombre=request.form['nombre'].capitalize(),cantidad=int(request.form['Cantidad']),unidad=request.form['unidad'],recetaID=int(request.form['idreceta']))
        db.session.add(ingredienteNuevo)
        db.session.commit()
        nroI += 1
        return render_template('ingredientes.html', Nombre=(sesion.unusuario.nombre),idreceta=request.form['idreceta'],ingredientes = nroI,mensaje = 'Ingrediente nro {} agregado con exito'.format(nroI))
    elif nroI == 10:
        return render_template('ingredientes.html', Nombre=(sesion.unusuario.nombre),idreceta=request.form['idreceta'],ingredientes = nroI,mensaje = 'Ha alcanzado el limite de ingredientes')
    else:
        return render_template('ingredientes.html', Nombre=(sesion.unusuario.nombre),idreceta=request.form['idreceta'],ingredientes = nroI,mensaje = 'Algo ocurrio, intente nuevamente')



@app.route('/ConsultarRanking',methods = ['GET','POST'])
def Ranking():#Hecha
    return render_template('Consultar.html',Nombre=sesion.unusuario.nombre,recetas = receta.query.order_by(receta.cantidadmegusta.desc()).limit(5))

#Consultar receta por tiempo de elaboracion ingresado atraves de NavBar
@app.route('/ConsultarReceta',methods = ['GET','POST'])
def consultarReceta():
    return render_template('IngresarTiempo.html',Nombre=sesion.unusuario.nombre)

@app.route('/ConsultaElaboracion',methods = ['GET','POST'])
def recetasTiempoElaboracion():
    tiempoE = int(request.form['tiempo'])
    return render_template('ConsultaTiempo.html',Nombre=sesion.unusuario.nombre ,recetas = receta.query.filter(receta.tiempo < tiempoE).all())

@app.route('/infoReceta',methods = ['GET','POST'])
def infoReceta():
    idreceta = int(request.form['id'])
    name="info1"
    return render_template('InfoReceta.html',Nombre=sesion.unusuario.nombre,receta = receta.query.filter_by(id=idreceta).first(),name=name)
@app.route('/megusta',methods = ['GET','POST'])
def megusta():
    
    receta.query.filter_by(id=request.form['id']).first().cantidadmegusta += 1
    id1.id = request.form['id']
    db.session.commit()
    return redirect('/infoReceta2')
@app.route('/infoReceta2',methods = ['GET','POST'])
def infoReceta2():
    idreceta = id1.id
    name="info2"
    return render_template('InfoReceta.html',Nombre=sesion.unusuario.nombre,receta = receta.query.filter_by(id=idreceta).first(),name=name)   

    
    

#Consultar receta por ingrediente ingresado atraves de NavBar
@app.route('/ConsultarRecetaIngrediente',methods = ['GET','POST'])
def consultarRecetaPorIngrediente():
    return render_template('IngresarIngredienteTeclado.html', Nombre=sesion.unusuario.nombre)

@app.route('/RecetaPorIngrediente',methods = ['GET','POST'])
def mostrarRecetasPorIngrediente():
    nombreI =request.form['NombreIngrediente'].capitalize()
    nombreI="%{}%".format(nombreI)
    receta1= receta.query.join(receta.ingrediente).filter(ingrediente.nombre.like(nombreI)).all()
    return render_template("ConsultarIngrediente.html", Nombre=sesion.unusuario.nombre,recetas = receta1)


if __name__=='__main__':
    
    db.create_all()
    app.run(debug=True)
