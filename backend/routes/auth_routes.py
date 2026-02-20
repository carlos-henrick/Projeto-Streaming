from flask import Blueprint, request, jsonify
from database.db_connection import db
from models.tabelas import Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
import re   

auth_bp = Blueprint('auth', __name__)



def validar_email(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None

def validar_senha(senha):
    if len(senha) < 8:
        return False
    if not re.search(r"[A-Z]", senha):
        return False
    if not re.search(r"[0-9]", senha):
        return False
    if not re.search(r"[@$!%*?&]", senha):
        return False
    return True



# registro


@auth_bp.route('/register', methods=['POST'])
def register():
    dados = request.get_json() or {}             

    nome = dados.get('nome', '').strip()
    email = dados.get('email', '').strip().lower()
    senha = dados.get('senha', '').strip()

    if not nome or not email or not senha:
        return jsonify({"error": "Nome, email e senha são obrigatórios."}), 400


    if not validar_email(email):
        return jsonify({"error": "Email inválido."}), 400

    if not validar_senha(senha):
        return jsonify({
            "error": "Requisitos: mínimo 8 caracteres, letra maiúscula, número e símbolo."
        }), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"error": "Email já cadastrado."}), 400

   
    usuario = Usuario(
        nome=nome,
        email=email,
        senha=generate_password_hash(senha),
        role='user'
    )

    db.session.add(usuario)
    db.session.commit()

    return jsonify({"message": "Usuário criado com sucesso!"}), 201


# login

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    email = data.get("email", "").strip().lower()
    senha = data.get("senha", "").strip()

    if not email or not senha:
        return jsonify({"error": "Email e senha são obrigatórios."}), 400

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not check_password_hash(usuario.senha, senha):
        return jsonify({"error": "Credenciais inválidas."}), 401

    access_token = create_access_token(
        identity=str(usuario.id),
        additional_claims={"role": usuario.role}
    )

    return jsonify({
        "access_token": access_token,
        "user": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "role": usuario.role
        }
    }), 200