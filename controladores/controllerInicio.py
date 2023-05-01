from app import app, db
from modelos.categoria import *
from modelos.producto import *
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

#Valida que no exista la base de datos para crearla
with app.app_context():
    db.create_all()

@app.route("/")
def inicio():
    return render_template("inicio.html")
