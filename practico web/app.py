from re import template
from venv import create
from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
import hashlib


app=Flask(__name__)
app.config.from_pyfile("config.py")

from models import db
from models import usuario,receta,ingrediente

@app.route('/')
def login():
    return render_template('Log-in.html')


@app.route('/inicio',methods=['GET','POST'])
def checklogin():  # check if user is in database   
    password=request.form['passwrd']
    password2=hashlib.md5(bytes(password,encoding='utf-8')).hexdigest()
    
    user = usuario.query.filter_by(correo = request.form['mail']).first()
    if user is not None:
        print(password2)
        print(user.clave)
        if user.clave==password2:
            return render_template('NavBar.html')
        else:
            return render_template('Error.html', error = 'Password invalid')
    else:
        return render_template('Error.html', error = 'User invalid')
@app.route('/pagina_principal')
def pagina_principal():
    return render_template('NavBar.html')




#Ingresar Receta atraves de NavBar
@app.route('/IngresarReceta',methods=['GET','POST'])
def ingresarReceta():
    return render_template('Errorctrl.html', error = 'Funcionalidad sin terminar')

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
    app.run()
