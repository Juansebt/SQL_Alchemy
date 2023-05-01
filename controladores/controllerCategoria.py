from app import app, db
from modelos.categoria import *
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc


@app.route("/vistaCategoria")
def vistaCategoria():
    return render_template("frmCategoria.html")

@app.route("/agregarCategoria", methods=["POST"])
def agregarCategoria():
    mensaje = ""
    estado = False
    try:
        nombre = request.form["txtNombre"].upper()
        cat = categoria(catNombre=nombre) #objeto categoria
        db.session.add(cat)
        db.session.commit()
        mensaje = f"La categoria {nombre} se ha agregado correctamente"
        estado = True
    except exc.SQLAlchemyError as error:
        db.session.rollback()
        mensaje = str(error)
    return render_template("frmCategoria.html",mensaje=mensaje, estado= estado)

# ·····························································································································································

@app.route("/obtenerCategoriasJson", methods=["GET"])
def obtenerCategorias():
    listaCategorias = categoria.query.all()
    listaJson = []
    
    for cat in listaCategorias:
        cat = {
            "idCategoria":cat.idCategoria,
            "catNombre":cat.catNombre
        }
    
        listaJson.append(cat)
    
    return listaJson

@app.route("/agregarCategoriaJson", methods=["POST"])
def agregarCategoriaJson():
    try:
        datos = request.get_json()
        print(datos)
        
        cat = categoria(catNombre = datos["nombreCategoria"])
        
        db.session.add(cat)
        db.session.commit()
        mensaje = f"Categoria agregada"
    
    except exc.SQLAlchemyError as error:
        db.session.rollback()
        mensaje = f"Porblemas al agregar categoria. Error: {error}"
        
    return {"mensaje":mensaje}