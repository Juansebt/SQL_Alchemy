from app import app, db
from modelos.categoria import *
from modelos.producto import *
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from werkzeug.utils import secure_filename
import os

@app.route("/vistaProducto")
def vistaProducto():
    product = None
    listaCategorias = categoria.query.all()
    return render_template("frmProducto.html", producto=product, listaCategorias=listaCategorias)

@app.route("/listarProductos", methods=["GET"])
def listarProductos():
    listaProductos = producto.query.all()
    return render_template("listarProductos.html", listaProductos=listaProductos)

@app.route("/agregarProducto", methods=["POST"])
def agregarProducto():
    estado = False
    mensaje = ""
    try:
        codigo = int(request.form["txtCodigo"])
        nombre = request.form["txtNombreP"]
        precio = int(request.form["txtPrecio"])
        categ = request.form["cbCategoria"]
        
        product = producto(proCodigo=codigo,
                           proNombre=nombre,
                           proPrecio=precio,
                           proCategoria=categ)
        
        db.session.add(product)
        db.session.commit()
        
        archivo = request.files["fileFoto"]
        if(archivo.filename!=""):
            nombreFile = secure_filename(archivo.filename)
            nombreArchivo = str(product.idProducto)+".jpg"
            archivo.save(os.path.join(app.config["UPLOAD_FOLDER"],nombreArchivo))
        mensaje = f"Se ha agregado correctamente el producto"
        estado = True
        # return redirect("/listarProductos")
        listaProductos = producto.query.all()
        return render_template("listarProductos.html", listaProductos=listaProductos, estado=estado, mensaje=mensaje)
            
    except exc.SQLAlchemyError as error:
        db.session.rollback()
        mensaje = str(error)
    listaCategorias = categoria.query.all()
    return render_template("frmProducto.html", producto=product, listaCategorias=listaCategorias, mensaje=mensaje, estado=estado)

@app.route("/consultarProducto/<int:idProducto>")
def consultarProducto(idProducto):
    try:
        product = producto.query.get(idProducto)
    except exc.SQLAlchemyError as error:
        mensaje = str(error)
    listaCategorias = categoria.query.all()
    return render_template("frmEditarProducto.html",producto=product,listaCategorias=listaCategorias)

@app.route("/actualizarProducto", methods=["POST"])
def actualizarProducto():
    estado = False
    mensaje = ""
    try:
        idProducto = int(request.form["idProducto"])
        product = producto.query.get(idProducto) #consulta
        
        #valores nuevos
        product.proCodigo = int(request.form["txtCodigo"])
        product.proNombre = request.form["txtNombreP"]
        product.proPrecio = int(request.form["txtPrecio"])
        product.proCategoria = int(request.form["cbCategoria"])
        
        db.session.commit() #actualizar
        
        archivo = request.files["fileFoto"]
        if(archivo.filename!=""):
            nombreFile = secure_filename(archivo.filename)
            nombreArchivo = str(product.idProducto)+".jpg"
            archivo.save(os.path.join(app.config["UPLOAD_FOLDER"],nombreArchivo))
        mensaje = f"Producto Actualizado"
        estado = True
        # return redirect("/listarProductos")
        listaProductos = producto.query.all()
        return render_template("listarProductos.html", listaProductos=listaProductos, estado=estado, mensaje=mensaje)
        
    except exc.SQLAlchemyError as error:
        db.session.rollback()
        mensaje = f"Problemas al actualizar producto {str(error)}"
    
    listaProductos = producto.query.all()
    return render_template("listarProductos.html", listaProductos=listaProductos, estado=estado, mensaje=mensaje)

@app.route("/eliminar/<int:idProducto>")
def eliminar(idProducto):
    mensaje = ""
    estado = False
    try:
        product = producto.query.get(idProducto)
        db.session.delete(product)
        db.session.commit()
        nombreArchivo = str(idProducto)+".jpg"
        os.remove(os.path.join(app.config["UPLOAD_FOLDER"]+"/"+nombreArchivo))
        estado =  True
        mensaje = f"Producto eliminado correctamente"
        listaProductos = producto.query.all()
        return render_template("listarProductos.html",listaProductos=listaProductos, estado=estado, mensaje=mensaje)
        
    except exc.SQLAlchemyError as error:
        db.session.rollback()
        mensaje = error
    
    listaProductos = producto.query.all()
    return render_template("listarProductos.html", listaProductos=listaProductos, estado=estado, mensaje=mensaje)

# ···································································································································································································

@app.route("/listarProductosJson", methods=["GET"])
def listarProductosJson():
    mensaje = "PRODUCTOS"
    try:
        listaProductos = producto.query.all()
        listaJson = []
        for product in listaProductos:
            product = {
                "idProducto":product.idProducto,
                "proNombre":product.proNombre,
                "proPrecio":product.proPrecio,
                "categoria": {
                    "idCategoria": product.categoria.idCategoria,
                    "catNombre": product.categoria.catNombre
                }
            }
            listaJson.append(product)
            
    except exc.SQLAlchemyError as error:
        mensaje = "Problemas a obtener los productos"
        
    return {"mensaje":mensaje,"listaProductos":listaJson}

@app.route("/consultarProductoJson", methods=["GET"])
def consultarProductoJson():
    try:
        datos = request.get_json(force=True)
        idProducto = int(datos["idProducto"])
        product = producto.query.get(idProducto)
        productJson = {
            "idProducto":product.idProducto,
            "proNombre":product.proNombre,
            "proPrecio":product.proPrecio,
            "categoria": {
                "idCategoria": product.categoria.idCategoria,
                "catNombre": product.categoria.catNombre
            }
        }
        mensaje = f"Datos del producto"
        
    except exc.SQLAlchemyError as error:
        mensaje = f"Problemas al consultar"
        
    return {"mensaje":mensaje,"producto":productJson}

@app.route("/agregarProductoJson", methods=["POST"])
def agregarProductoJson():
    estado = False
    try:
        datos = request.get_json(force=True)
        codigo = int(datos["codigo"])
        nombre = datos["nombre"]
        precio = int(datos["precio"])
        cat = int(datos["categoria"])
        product = producto(proCodigo=codigo,proNombre=nombre,proPrecio=precio,proCategoria=cat)
        
        db.session.add(product)
        db.session.commit()
        mensaje = f"Producto agregado correctamente"
        estado = True
        
    except exc.SQLAlchemyError as error:
        db.session.rollback()
        mensaje = f"Problemas al registrar"
        
    return {"mensaje":mensaje,"estado":estado}

@app.route("/eliminarProductoJson", methods=["POST"])
def eliminarProductoJson():
    estado = False
    try:
        datos = request.get_json(force=True)
        idProducto = int(datos["idProducto"])
        product = producto.query.get(idProducto)
        
        db.session.delete(product)
        db.session.commit()
        estado = True
        mensaje = f"Producto eliminado"
        
        nombreArchivo = str(idProducto)+".jpg"
        os.remove(os.path.join(app.config["UPLOAD_FOLDER"]+"/"+nombreArchivo))
        
    except exc.SQLAlchemyError as error:
        db.session.rollback()
        mensaje = f"Problemas al eliminar el producto"
    
    return {"mensaje":mensaje,"estado":estado}

@app.route("/actualizarProductoJson", methods=["POST"])
def actualizarProductoJson():
    estado = False
    try:
        datos = request.get_json(force=True)
        idProducto = int(datos["idProducto"])
        product = producto.query.get(idProducto)
        product.proCodigo = int(datos["codigo"])
        product.proNombre = datos["nombre"]
        product.proPrecio = int(datos["precio"])
        product.proCategoria = int(datos["categoria"])
        
        db.session.commit()
        estado = True
        mensaje = f"Producto actualizado"
        
    except exc.SQLAlchemyError as error:
        db.session.rollback()
        mensaje = f"Problemas al actualizar el producto"
        
    return {"mensaje":mensaje,"estado":estado}