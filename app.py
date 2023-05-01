from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
import sqlite3

app = Flask(__name__)

#MySQL
# cadenaConexion = "mysql+pymysql://root@localhost/tienda_sqlalchemy"

#MySQL Lite
cadenaConexion = "sqlite:///basedatos.db"

app.config["SQLALCHEMY_DATABASE_URI"] = cadenaConexion

app.config['UPLOAD_FOLDER']='./static/images'


db = SQLAlchemy(app)

from controladores.controllerInicio import *
from controladores.controllerCategoria import *
from controladores.controllerProducto import *

#iniciar el servidor web
if __name__=='__main__':
    app.run(host="0.0.0.0",port=3000,debug=True)