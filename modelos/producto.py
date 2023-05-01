from app import app,db

class producto(db.Model):
    __tablename__ = "productos"
    idProducto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    proCodigo = db.Column(db.Integer, unique=True, nullable=True)
    proNombre = db.Column(db.String(50), nullable=False)
    proPrecio = db.Column(db.Integer, nullable=True)
    
    proCategoria = db.Column(db.Integer, db.ForeignKey('categorias.idCategoria'), nullable=False) #campo foraneo
    
    categoria = db.relationship("categoria",backref=db.backref('categorias', lazy=True)) #relacionar con la tabla categorias