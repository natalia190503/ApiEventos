from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from datetime import datetime

db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    role = db.Column(Enum('admin', 'organizer', 'attendee',
                     name='role_enum'), nullable=False, default='attendee')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Método para serializar el objeto a un formato de diccionario
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'address': self.address,
            'role': self.role,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Evento(db.Model):
    __tablename__ = 'eventos'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    organizer_id = db.Column(
        db.BigInteger, db.ForeignKey('usuarios.id'), nullable=False)
    tittle = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.String(150))
    start_time = db.Column(db.TIMESTAMP)
    end_time = db.Column(db.TIMESTAMP)
    place_id = db.Column(db.BigInteger)  # Relacionar con tabla de Lugares
    # Relacionar con tabla de Categorías
    category_id = db.Column(db.BigInteger)
    status = db.Column(db.String(50))
    created_at = db.Column(db.TIMESTAMP, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, nullable=False,
                           default=datetime.utcnow, onupdate=datetime.utcnow)

    # Método para serializar el objeto a un formato de diccionario
    def serialize(self):
        return {
            'id': self.id,
            'organizer_id': self.organizer_id,
            'tittle': self.tittle,
            'description': self.description,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'place_id': self.place_id,
            'category_id': self.category_id,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Lugar(db.Model):
    __tablename__ = 'lugares'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(150))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    capacity = db.Column(db.Integer)
    created_at = db.Column(db.TIMESTAMP, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, nullable=False,
                           default=datetime.utcnow, onupdate=datetime.utcnow)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'country': self.country,
            'capacity': self.capacity,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(150))
    created_at = db.Column(db.TIMESTAMP, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, nullable=False,
                           default=datetime.utcnow, onupdate=datetime.utcnow)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Inscripcion(db.Model):
    __tablename__ = 'inscripciones'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    event_id = db.Column(db.BigInteger, nullable=False)  # FK a eventos
    assistant_id = db.Column(db.BigInteger, nullable=False)  # FK a usuarios
    status = db.Column(db.String(50))
    created_at = db.Column(db.TIMESTAMP, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, nullable=False,
                           default=datetime.utcnow, onupdate=datetime.utcnow)

    def serialize(self):
        return {
            'id': self.id,
            'event_id': self.event_id,
            'assistant_id': self.assistant_id,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Entrada(db.Model):
    __tablename__ = 'entradas'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    registration_id = db.Column(db.BigInteger)
    type = db.Column(db.String(150))
    price = db.Column(db.Float)
    created_at = db.Column(db.TIMESTAMP, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, nullable=False,
                           default=datetime.utcnow, onupdate=datetime.utcnow)

    def serialize(self):
        return {
            'id': self.id,
            'registration_id': self.registration_id,
            'type': self.type,
            'price': self.price,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
