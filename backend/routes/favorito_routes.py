from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.favorito_service import FavoritoService

favorito_bp = Blueprint("favoritos", __name__, url_prefix="/favoritos")

@favorito_bp.route("", methods=["POST"])
@jwt_required()
def adicionar():
    usuario_id = get_jwt_identity()
    dados = request.get_json()

    try:
        favorito = FavoritoService.adicionar(usuario_id, dados)
        return jsonify({"msg": "Adicionado aos favoritos"}), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400



@favorito_bp.route("/<int:favorito_id>", methods=["DELETE"])
@jwt_required()
def remover(favorito_id):
    usuario_id = get_jwt_identity()

    try:
        FavoritoService.remover(usuario_id, favorito_id)
        return jsonify({"msg": "Removido dos favoritos"})
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404


@favorito_bp.route("", methods=["GET"])
@jwt_required()
def listar():
    usuario_id = get_jwt_identity()
    favoritos = FavoritoService.listar(usuario_id)
    return jsonify(favoritos)