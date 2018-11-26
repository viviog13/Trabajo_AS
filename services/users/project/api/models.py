# services/users/project/api/models.py
from sqlalchemy.sql import func


from project import db


class User(db.Model):

    __tablename__ = 'libros'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(128), nullable=False)
    autor = db.Column(db.String(128), nullable=False)
    añodepublicacion = db.Column(db.String(128), nullable=False)
    editorial = db.Column(db.String(128), nullable=False)
    generoliterario = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'autor': self.autor,
            'añodepublicacion': self.añodepublicacion,
            'editorial': self.editorial,
            'generoliterario': self.generoliterario,
            'active': self.active
        }

    def __init__(
        self, titulo, autor, añodepublicacion,
        editorial, generoliterario
    ):

        self.titulo = titulo
        self.autor = autor
        self.añodepublicacion = añodepublicacion
        self.editorial = editorial
        self.generoliterario = generoliterario
