from app import app,db

class categoria(db.Model):
    __tablename__ = "categorias" #nombre de la tabla
    idCategoria = db.Column(db.Integer, primary_key=True, autoincrement=True) #columna de la id
    catNombre = db.Column(db.String(50), unique=True, nullable=False) #columna del nombre
    
    def __repr__(self):
        return f'{self.catNombre}'
    