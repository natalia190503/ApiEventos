from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Usuario, Evento, Lugar, Categoria, Inscripcion, Entrada
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuración de base de datos (modifica los valores según tu entorno)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/eventosdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# ---------------------- USUARIOS ----------------------


@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([u.serialize() for u in usuarios]), 200


@app.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    return jsonify(usuario.serialize()), 200


@app.route('/usuarios', methods=['POST'])
def add_usuario():
    data = request.get_json()
    nuevo = Usuario(
        name=data['name'],
        email=data['email'],
        password=data['password'],
        address=data['address'],
        role=data.get('role', 'attendee')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'message': 'Usuario creado', 'id': nuevo.id}), 201


@app.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    data = request.get_json()
    usuario.name = data.get('name', usuario.name)
    usuario.email = data.get('email', usuario.email)
    usuario.password = data.get('password', usuario.password)
    usuario.address = data.get('address', usuario.address)
    usuario.role = data.get('role', usuario.role)

    db.session.commit()

    return jsonify({
        'message': 'Usuario actualizado',
        'updated_at': usuario.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    }), 200


@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'message': 'Usuario eliminado'}), 200

# ---------------------- EVENTOS ----------------------


# Obtener todos los eventos
@app.route('/eventos', methods=['GET'])
def get_eventos():
    eventos = Evento.query.all()
    return jsonify([e.serialize() for e in eventos]), 200


# Obtener un evento por ID
@app.route('/eventos/<int:id>', methods=['GET'])
def get_evento(id):
    evento = db.session.get(Evento, id)
    if not evento:
        return jsonify({'message': 'Evento no encontrado'}), 404
    return jsonify(evento.serialize()), 200


# Crear un nuevo evento
@app.route('/eventos', methods=['POST'])
def add_evento():
    data = request.get_json()

    required_fields = ['organizer_id', 'tittle',
                       'start_time', 'end_time', 'place_id', 'category_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Campo obligatorio faltante: {field}'}), 400

    try:
        nuevo = Evento(
            organizer_id=int(data['organizer_id']),
            tittle=data['tittle'],
            description=data.get('description', ''),
            start_time=datetime.fromisoformat(data['start_time']),
            end_time=datetime.fromisoformat(data['end_time']),
            place_id=int(data['place_id']),
            category_id=int(data['category_id']),
            status=data.get('status', 'activo')
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({'message': 'Evento creado', 'id': nuevo.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al crear el evento: {str(e)}'}), 500


# Actualizar un evento
@app.route('/eventos/<int:id>', methods=['PUT'])
def update_evento(id):
    evento = db.session.get(Evento, id)
    if not evento:
        return jsonify({'message': 'Evento no encontrado'}), 404

    data = request.get_json()

    try:
        evento.organizer_id = data.get('organizer_id', evento.organizer_id)
        evento.tittle = data.get('tittle', evento.tittle)
        evento.description = data.get('description', evento.description)

        if 'start_time' in data:
            evento.start_time = datetime.fromisoformat(data['start_time'])
        if 'end_time' in data:
            evento.end_time = datetime.fromisoformat(data['end_time'])

        evento.place_id = data.get('place_id', evento.place_id)
        evento.category_id = data.get('category_id', evento.category_id)
        evento.status = data.get('status', evento.status)

        db.session.commit()
        return jsonify({'message': 'Evento actualizado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al actualizar el evento: {str(e)}'}), 500


# Eliminar un evento
@app.route('/eventos/<int:id>', methods=['DELETE'])
def delete_evento(id):
    evento = db.session.get(Evento, id)
    if not evento:
        return jsonify({'message': 'Evento no encontrado'}), 404
    try:
        db.session.delete(evento)
        db.session.commit()
        return jsonify({'message': 'Evento eliminado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al eliminar el evento: {str(e)}'}), 500


# ---------------------- LUGARES ----------------------


@app.route('/lugares', methods=['GET'])
def get_lugares():
    lugares = Lugar.query.all()
    return jsonify([l.serialize() for l in lugares]), 200


@app.route('/lugares/<int:id>', methods=['GET'])
def get_lugar(id):
    lugar = Lugar.query.get(id)
    if not lugar:
        return jsonify({'message': 'Lugar no encontrado'}), 404
    return jsonify(lugar.serialize()), 200


@app.route('/lugares', methods=['POST'])
def add_lugar():
    data = request.get_json()
    nuevo = Lugar(
        name=data['name'],
        address=data['address'],
        city=data['city'],
        country=data['country'],
        capacity=data['capacity']
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'message': 'Lugar creado', 'id': nuevo.id}), 201


@app.route('/lugares/<int:id>', methods=['PUT'])
def update_lugar(id):
    lugar = Lugar.query.get(id)
    if not lugar:
        return jsonify({'message': 'Lugar no encontrado'}), 404
    data = request.get_json()
    lugar.name = data.get('name', lugar.name)
    lugar.address = data.get('address', lugar.address)
    lugar.city = data.get('city', lugar.city)
    lugar.country = data.get('country', lugar.country)
    lugar.capacity = data.get('capacity', lugar.capacity)
    db.session.commit()
    return jsonify({'message': 'Lugar actualizado', 'updated_at': lugar.updated_at.strftime('%Y-%m-%d %H:%M:%S')}), 200


@app.route('/lugares/<int:id>', methods=['DELETE'])
def delete_lugar(id):
    lugar = Lugar.query.get(id)
    if not lugar:
        return jsonify({'message': 'Lugar no encontrado'}), 404
    db.session.delete(lugar)
    db.session.commit()
    return jsonify({'message': 'Lugar eliminado'}), 200


# ---------------------- CATEGORÍAS ----------------------
@app.route('/categorias', methods=['GET'])
def get_categorias():
    categorias = Categoria.query.all()
    return jsonify([c.serialize() for c in categorias]), 200


@app.route('/categorias/<int:id>', methods=['GET'])
def get_categoria(id):
    categoria = db.session.get(Categoria, id)
    if not categoria:
        return jsonify({'message': 'Categoría no encontrada'}), 404
    return jsonify(categoria.serialize()), 200


@app.route('/categorias', methods=['POST'])
def add_categoria():
    data = request.get_json()
    nueva = Categoria(
        name=data['name'],
        description=data.get('description', '')
    )
    db.session.add(nueva)
    db.session.commit()
    return jsonify({'message': 'Categoría creada', 'id': nueva.id}), 201


@app.route('/categorias/<int:id>', methods=['PUT'])
def update_categoria(id):
    categoria = db.session.get(Categoria, id)
    if not categoria:
        return jsonify({'message': 'Categoría no encontrada'}), 404
    data = request.get_json()
    categoria.name = data.get('name', categoria.name)
    categoria.description = data.get('description', categoria.description)
    db.session.commit()
    return jsonify({'message': 'Categoría actualizada'}), 200


@app.route('/categorias/<int:id>', methods=['DELETE'])
def delete_categoria(id):
    categoria = db.session.get(Categoria, id)
    if not categoria:
        return jsonify({'message': 'Categoría no encontrada'}), 404
    db.session.delete(categoria)
    db.session.commit()
    return jsonify({'message': 'Categoría eliminada'}), 200


# ---------------------- INSCRIPCIONES ----------------------

@app.route('/inscripciones', methods=['GET'])
def get_inscripciones():
    inscripciones = Inscripcion.query.all()
    return jsonify([i.serialize() for i in inscripciones]), 200


@app.route('/inscripciones/<int:id>', methods=['GET'])
def get_inscripcion(id):
    inscripcion = Inscripcion.query.get(id)
    if not inscripcion:
        return jsonify({'message': 'Inscripción no encontrada'}), 404
    return jsonify(inscripcion.serialize()), 200


@app.route('/inscripciones', methods=['POST'])
def add_inscripcion():
    data = request.get_json()
    nueva = Inscripcion(
        event_id=data['event_id'],
        assistant_id=data['assistant_id'],
        status=data.get('status', 'inscrito')
    )
    db.session.add(nueva)
    db.session.commit()
    return jsonify({'message': 'Inscripción creada', 'id': nueva.id}), 201


@app.route('/inscripciones/<int:id>', methods=['PUT'])
def update_inscripcion(id):
    inscripcion = Inscripcion.query.get(id)
    if not inscripcion:
        return jsonify({'message': 'Inscripción no encontrada'}), 404

    data = request.get_json()
    inscripcion.event_id = data.get('event_id', inscripcion.event_id)
    inscripcion.assistant_id = data.get(
        'assistant_id', inscripcion.assistant_id)
    inscripcion.status = data.get('status', inscripcion.status)

    db.session.commit()
    return jsonify({'message': 'Inscripción actualizada'}), 200


@app.route('/inscripciones/<int:id>', methods=['DELETE'])
def delete_inscripcion(id):
    inscripcion = Inscripcion.query.get(id)
    if not inscripcion:
        return jsonify({'message': 'Inscripción no encontrada'}), 404

    db.session.delete(inscripcion)
    db.session.commit()
    return jsonify({'message': 'Inscripción eliminada'}), 200

# ---------------------- ENTRADAS ----------------------


# Ruta GET para todas las entradas
@app.route('/entradas', methods=['GET'])
def get_entradas():
    entradas = Entrada.query.all()
    return jsonify([e.serialize() for e in entradas]), 200

# Ruta GET para una entrada por id


@app.route('/entradas/<int:id>', methods=['GET'])
def get_entrada(id):
    entrada = Entrada.query.get(id)
    if not entrada:
        return jsonify({'message': 'Entrada no encontrada'}), 404
    return jsonify(entrada.serialize()), 200

# Ruta POST para agregar una nueva entrada


@app.route('/entradas', methods=['POST'])
def add_entrada():
    data = request.get_json()
    try:
        nueva = Entrada(
            # Asegúrate de usar el nombre correcto
            registration_id=data['registration_id'],
            type=data['type'],
            price=data['price']
        )
        db.session.add(nueva)
        db.session.commit()
        return jsonify({'message': 'Entrada creada', 'id': nueva.id}), 201
    except KeyError as e:
        return jsonify({'message': f'Error en los datos: {e}'}), 400

# Ruta PUT para actualizar una entrada


@app.route('/entradas/<int:id>', methods=['PUT'])
def update_entrada(id):
    entrada = Entrada.query.get(id)
    if not entrada:
        return jsonify({'message': 'Entrada no encontrada'}), 404
    data = request.get_json()
    entrada.registration_id = data.get(
        'registration_id', entrada.registration_id)
    entrada.type = data.get('type', entrada.type)
    entrada.price = data.get('price', entrada.price)
    db.session.commit()
    return jsonify({'message': 'Entrada actualizada'}), 200

# Ruta DELETE para eliminar una entrada


@app.route('/entradas/<int:id>', methods=['DELETE'])
def delete_entrada(id):
    entrada = Entrada.query.get(id)
    if not entrada:
        return jsonify({'message': 'Entrada no encontrada'}), 404
    db.session.delete(entrada)
    db.session.commit()
    return jsonify({'message': 'Entrada eliminada'}), 200


# ---------------------- MAIN ----------------------
if __name__ == '__main__':
    app.run(debug=True)
