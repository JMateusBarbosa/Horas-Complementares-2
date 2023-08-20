from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

# Exemplo de armazenamento temporário de usuários (substituir por um banco de dados)
users = []

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    # Hash da senha antes de armazenar
    hashed_password = generate_password_hash(password, method='sha256')

    users.append({'username': username, 'password': hashed_password})

    return jsonify({'message': 'Usuário registrado com sucesso!'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    user = next((user for user in users if user['username'] == username), None)
    if user and check_password_hash(user['password'], password):
        return jsonify({'message': 'Login bem-sucedido!'})

    return jsonify({'message': 'Credenciais inválidas'}), 401
