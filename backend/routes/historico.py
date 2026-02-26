from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.http import erro_resposta
from services.historico_service import HistoricoService

historico_bp = Blueprint("historico", __name__)


# BUSCAR PROGRESSO 

@historico_bp.route("/progresso/<tipo>/<int:midia_id>", methods=["GET"])
@jwt_required()
def buscar_progresso(tipo, midia_id):
    usuario_id = get_jwt_identity()
    dados = HistoricoService.buscar_progresso(usuario_id, tipo, midia_id)
    return jsonify(dados), 200



# ATUALIZAR PROGRESSO 

@historico_bp.route("/progresso", methods=["POST"])
@jwt_required()
def atualizar_progresso():
    usuario_id = get_jwt_identity()
    dados = request.get_json() or {}

    obrigatorios = ["tipo_midia", "midia_id", "tempo_atual"]
    erros = [f"{c} é obrigatório." for c in obrigatorios if c not in dados]

    if erros:
        return erro_resposta(erros)

    try:
        h = HistoricoService.atualizar_progresso(usuario_id, dados)
    except ValueError as e:
        return erro_resposta([str(e)])

    return jsonify({
        "tempo_atual": h.tempo_atual,
        "finalizado": h.finalizado
    }), 200


# CONTINUAR ASSISTINDO

@historico_bp.route("/continuar", methods=["GET"])
@jwt_required()
def continuar_assistindo():
    usuario_id = get_jwt_identity()
    historicos = HistoricoService.listar_continuar(usuario_id)

    return jsonify([
        {
            "tipo_midia": h.tipo_midia,
            "midia_id": h.midia_id,
            "tempo_atual": h.tempo_atual,
            "finalizado": h.finalizado,
            "updated_at": h.updated_at.isoformat()
        }
        for h in historicos
    ]), 200


# LISTAR HISTÓRICO 

@historico_bp.route("", methods=["GET"])
@jwt_required()
def listar_historico():
    usuario_id = get_jwt_identity()
    historicos = HistoricoService.listar_historico(usuario_id)

    return jsonify([
        {
            "tipo_midia": h.tipo_midia,
            "midia_id": h.midia_id,
            "tempo_atual": h.tempo_atual,
            "finalizado": h.finalizado,
            "updated_at": h.updated_at.isoformat()
        }
        for h in historicos
    ]), 200
