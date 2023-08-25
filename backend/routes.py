from flask import Blueprint, make_response, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from auth_utils import jwt_required  # Importe o jwt_required do arquivo auth_utils
import jwt
import datetime
import json
import secrets

# Gera uma chave aleatória de 32 bytes (256 bits)
chave_secreta = secrets.token_hex(32)



auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')

    # Hash da senha antes de armazenar
    hashed_password = generate_password_hash(senha, method='sha256')

    aluno = {
        'nome': nome,
        'email': email,
        'senha': hashed_password
    }

    try:
        # Carregar os alunos existentes do arquivo, se existir
        with open('alunos_temp.json', 'r') as json_file:
            alunos = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existir ou não estiver no formato válido, começar com uma lista vazia
        alunos = []

    # Adicionar o novo aluno à lista
    alunos.append(aluno)

    # Escrever todos os alunos de volta no arquivo
    with open('alunos_temp.json', 'w') as json_file:
        json.dump(alunos, json_file, indent=2)

    return jsonify({'message': 'Aluno registrado com sucesso!'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    senha = data.get('senha')

    try:
        # Carregar os alunos existentes do arquivo, se existir
        with open('alunos_temp.json', 'r') as json_file:
            alunos = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        alunos = []

    # Verificar se o email está registrado e a senha está correta
    for aluno in alunos:
        if aluno['email'] == email and check_password_hash(aluno['senha'], senha):
            # Se as credenciais estão corretas, gerar um token de autenticação
            token_payload = {'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)}
            token = jwt.encode(token_payload, chave_secreta, algorithm='HS256')  # Substitua pela sua chave secreta

            return jsonify({'message': 'Login bem-sucedido', 'token': token})

    return jsonify({'message': 'Credenciais inválidas'}), 401



@auth_bp.route('/alunos', methods=['GET'])
def get_alunos():
    try:
        with open('alunos_temp.json', 'r') as json_file:
            alunos_temp = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        alunos_temp = []
    
    return make_response(
        jsonify(
            mensagem='Lista de alunos.',
            dados=alunos_temp
        )
    )
