from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils.permissions import admin_required

from validators.validators import (
    validar_string,
    validar_int_positivo,
    validar_data_iso
)
from utils.http import erro_resposta
from services.episodio_service import EpisodioService

episodios_bp = Blueprint("episodios", __name__)


# LISTAR EPISÓDIOS
@episodios_bp.route("/serie/<int:serie_id>", methods=["GET"])
def listar_episodios_por_serie(serie_id):
    try:
        episodios = EpisodioService.listar_por_serie(serie_id)
    except ValueError as e:
        return erro_resposta([str(e)], 404)

    return jsonify([
        {
            "id": e.id,
            "serie_id": e.serie_id,
            "temporada": e.temporada,
            "numero_episodio": e.numero_episodio,
            "titulo": e.titulo,
            "descricao": e.descricao,
            "duracao": e.duracao,
            "capa": e.capa,
            "data_lancamento": e.data_lancamento.isoformat(),
            "nome_arquivo_video": e.nome_arquivo_video
        }
        for e in episodios
    ]), 200


# ADICIONAR EPISÓDIO 
@episodios_bp.route("/adicionar", methods=["POST"])
@jwt_required()
@admin_required
def adicionar_episodio():
    dados = request.get_json() or {}
    erros = []

    serie_id = validar_int_positivo(dados.get("serie_id"), "Série")
    temporada = validar_int_positivo(dados.get("temporada"), "Temporada")
    numero = validar_int_positivo(dados.get("numero_episodio"), "Número do episódio")
    duracao = validar_int_positivo(dados.get("duracao"), "Duração")

    titulo = validar_string(dados.get("titulo"), "Título")
    descricao = validar_string(dados.get("descricao"), "Descrição")
    capa = validar_string(dados.get("capa"), "Capa")
    video = validar_string(dados.get("nome_arquivo_video"), "Arquivo de vídeo")
    data_lancamento, erro_data = validar_data_iso(dados.get("data_lancamento"))

    if not isinstance(serie_id, int):
        erros.append("Série inválida.")
    if not isinstance(temporada, int):
        erros.append("Temporada inválida.")
    if not isinstance(numero, int):
        erros.append("Número do episódio inválido.")
    if not isinstance(duracao, int):
        erros.append("Duração inválida.")

    for campo in [titulo, descricao,  video]:
        if not isinstance(campo, str):
            erros.append(campo)

    if erro_data or data_lancamento is None:
        erros.append("Data de lançamento inválida.")

    if erros:
        return erro_resposta(erros)

    payload = {
        "serie_id": serie_id,
        "temporada": temporada,
        "numero_episodio": numero,
        "titulo": titulo,
        "descricao": descricao,
        "duracao": duracao,
        "capa": capa,
        "data_lancamento": data_lancamento,
        "nome_arquivo_video": video
    }

    try:
        episodio = EpisodioService.criar(payload)
    except ValueError as e:
        return erro_resposta([str(e)], 409)

    return jsonify({"id": episodio.id}), 201


# EDITAR EPISÓDIO 
@episodios_bp.route("/editar/<int:episodio_id>", methods=["PUT"])
@jwt_required()
@admin_required
def editar_episodio(episodio_id):
    episodio = EpisodioService.obter_por_id(episodio_id)
    if not episodio:
        return erro_resposta(["Episódio não encontrado."], 404)

    dados = request.get_json() or {}
    atualizacao = {}
    erros = []

    campos_string = {
        "titulo": "Título",
        "descricao": "Descrição",
        "capa": "Capa",
        "nome_arquivo_video": "Arquivo de vídeo"
    }

    if "temporada" in dados or "numero_episodio" in dados:
        erros.append("Temporada e número do episódio não podem ser alterados.")
        
    for campo, nome in campos_string.items():
        if campo in dados:
            if dados[campo] is None:
                erros.append(f"{nome} não pode ser nulo.")
            else:
                valor = validar_string(dados[campo], nome)
                if not isinstance(valor, str):
                    erros.append(valor)
                else:
                    atualizacao[campo] = valor

    if "duracao" in dados:
        dur = validar_int_positivo(dados["duracao"], "Duração")
        if not isinstance(dur, int):
            erros.append("Duração inválida.")
        else:
            atualizacao["duracao"] = dur

    if "data_lancamento" in dados:
        if dados["data_lancamento"] is None:
            erros.append("Data de lançamento não pode ser nula.")
        else:
            data, erro = validar_data_iso(dados["data_lancamento"])
            if erro or data is None:
                erros.append("Data de lançamento inválida.")
            else:
                atualizacao["data_lancamento"] = data

    if erros:
        return erro_resposta(erros)

    EpisodioService.atualizar(episodio, atualizacao)
    return jsonify({"message": "Episódio atualizado com sucesso."}), 200


# DELETAR EPISÓDIO
@episodios_bp.route("/deletar/<int:episodio_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def deletar_episodio(episodio_id):
    episodio = EpisodioService.obter_por_id(episodio_id)
    if not episodio:
        return erro_resposta(["Episódio não encontrado."], 404)

    EpisodioService.deletar(episodio)
    return jsonify({"message": "Episódio deletado com sucesso."}), 200
