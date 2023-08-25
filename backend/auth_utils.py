from functools import wraps
import jwt
from flask import request, jsonify

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token de autenticação ausente'}), 401

        try:
            decoded_token = jwt.decode(token, 'seu_segredo_aqui', algorithms=['HS256'])
            # Aqui você pode acessar as informações do token, como o ID do usuário
            return f(decoded_token, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401

    return decorated_function
