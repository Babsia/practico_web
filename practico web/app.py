from re import template
from venv import create
from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
import hashlib
from almacenamiento import usuarioprueba

sesion=usuarioprueba()
app=Flask(__name__)
app.config.from_pyfile("config.py")

from models import db
from models import usuario,receta,ingrediente

@app.route('/')
def login():
    sesion.delusuario()
    return render_template('Log-in.html')


@app.route('/inicio',methods=['GET','POST'])
def checklogin():  # check if user is in database   
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
@app.route('/pagina_principal')
def pagina_principal():
    return render_template('NavBar.html', Nombre=(sesion.unusuario.nombre))




#Ingresar Receta atraves de NavBar
@app.route('/IngresarReceta',methods=['GET','POST'])
def ingresarReceta():#ingresar una receta y guardarla en la base de datos
    return render_template('ingresar.html', Nombre=(sesion.unusuario.nombre))

#Consultar 5 recetas con mas MG atraves de la NavBar
@app.route('/ConsultarRanking',methods = ['GET','POST'])
def consultarRanking():
    return render_template('Errorctrl.html', error = 'Funcionalidad sin terminar')

#Consultar receta por tiempo de elaboracion ingresado atraves de NavBar
@app.route('/ConsultarReceta',methods = ['GET','POST'])
def consultarReceta():
    return render_template('Errorctrl.html', error = 'Funcionalidad sin terminar')

#Consultar receta por ingrediente ingresado atraves de NavBar
@app.route('/ConsultarRecetaIngrediente',methods = ['GET','POST'])
def consultarRecetaPorIngrediente():
    return render_template('Errorctrl.html', error = 'Funcionalidad sin terminar')


if __name__=='__main__':
    
    db.create_all()
    app.run(debug=True)
