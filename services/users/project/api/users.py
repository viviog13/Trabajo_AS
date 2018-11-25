# services/users/project/api/users.py
from flask import Blueprint, jsonify, request, render_template

from project.api.models import User
from project import db
from sqlalchemy import exc

users_blueprint = Blueprint('users', __name__, template_folder='./templates')


@users_blueprint.route('/users/ping', methods=['GET'])
def ping_pong():
	return jsonify({
		'status': 'success',
		'message': 'pong'
	})


@users_blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@users_blueprint.route('/users', methods=['POST'])
def add_user():
    post_data = request.get_json()
    response_object = {
        'estado': 'fallo',
        'mensaje': 'Datos no validos.'
    }
    if not post_data:
        return jsonify(response_object), 400
    titulo = post_data.get('titulo')
    autor = post_data.get('autor')
    añodepublicacion = post_data.get('añodepublicacion')
    editorial = post_data.get('editorial')
    generoliterario = post_data.get('generoliterario')
    try:
        user = User.query.filter_by(autor=autor).first()
        if not user:
            db.session.add(User(titulo=titulo, autor=autor, añodepublicacion=añodepublicacion, editorial=editorial, generoliterario=generoliterario))
            db.session.commit()
            response_object['estado'] = 'satisfactorio'
            response_object['mensaje'] = f'{titulo} ha sido agregado!'
            return jsonify(response_object), 201
        else:
            response_object['mensaje'] = 'Datos no validos.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400

@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    """Obteniendo detalles de un unico usuario"""
    response_object = {
        'estado': 'fallo',
        'mensaje': 'Libro no existe'
    }

    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            return jsonify(response_object), 404
        else:
            response_object = {
                'estado': 'satisfactorio',
                'data': {
                    'id': user.id,
                    'titulo': user.titulo,
                    'autor': user.autor,
                    'añodepublicacion': user.añodepublicacion,
                    'editorial': user.editorial,
                    'generoliterario': user.generoliterario,
                    'active':user.active
                }
            }
            return jsonify(response_object), 200
    except ValueError:
    	return jsonify(response_object), 404

@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
	"""Obteniendo todos los usuarios"""
	response_object = {
	'estado': 'satisfactorio',
	'data': {
		'users': [user.to_json() for user in User.query.all()]
		}
	}
	return jsonify(response_object), 200