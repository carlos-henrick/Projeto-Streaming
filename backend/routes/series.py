from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils.permissions import admin_required

from validators.validators import (
    validar_string,
    validar_idade
)

from utils.http import erro_resposta
from services.serie_service import SerieService

series_bp = Blueprint("series", __name__)


# LISTAR SÉRIES
@series_bp.route("", methods=["GET"])
def listar_series():
    try:
        series = SerieService.listar(
            titulo=request.args.get("titulo", "").strip() or None,
            genero=request.args.get("genero", "").strip().lower() or None,
            idade_max=request.args.get("idade_max", type=int)
        )
    except ValueError as e:
        return erro_resposta([str(e)])

    return jsonify([
        {
            "id": s.id,
            "titulo": s.titulo,
            "descricao": s.descricao,
            "idade": s.idade,
            "genero": s.genero,
            "capa": s.capa
        }
        for s in series
    ]), 200


# ADICIONAR SÉRIE (TODOS OBRIGATÓRIOS)
@series_bp.route("/adicionar", methods=["POST"])
@jwt_required()
@admin_required
def adicionar_serie():
    dados = request.get_json() or {}
    erros = []

    titulo = validar_string(dados.get("titulo"), "Título")
    descricao = validar_string(dados.get("descricao"), "Descrição")
    genero = validar_string(dados.get("genero"), "Gênero")
    capa = validar_string(dados.get("capa"), "Capa")
    idade, erro_idade = validar_idade(dados.get("idade"))

    if not isinstance(titulo, str):
        erros.append(titulo)

    if not isinstance(descricao, str):
        erros.append(descricao)

    if not isinstance(genero, str):
        erros.append(genero)

    if not isinstance(capa, str):
        erros.append(capa)

    if erro_idade:
        erros.append(erro_idade)

    if erros:
        return erro_resposta(erros)

    payload = {
        "titulo": titulo,
        "descricao": descricao,
        "genero": genero.lower(),
        "capa": capa,
        "idade": idade
    }

    try:
        serie = SerieService.criar(payload)
    except ValueError as e:
        return erro_resposta([str(e)], 409)

    return jsonify({"id": serie.id}), 201


# EDITAR SÉRIE (PARCIAL)
@series_bp.route("/editar/<int:serie_id>", methods=["PUT"])
@jwt_required()
@admin_required
def editar_serie(serie_id):
    serie = SerieService.obter_por_id(serie_id)
    if not serie:
        return erro_resposta(["Série não encontrada."], 404)

    dados = request.get_json() or {}
    atualizacao = {}
    erros = []

    if "titulo" in dados:
        titulo = validar_string(dados["titulo"], "Título")
        if not isinstance(titulo, str):
            erros.append(titulo)
        else:
            atualizacao["titulo"] = titulo

    if "descricao" in dados:
        descricao = validar_string(dados["descricao"], "Descrição")
        if not isinstance(descricao, str):
            erros.append(descricao)
        else:
            atualizacao["descricao"] = descricao

    if "genero" in dados:
        genero = validar_string(dados["genero"], "Gênero")
        if not isinstance(genero, str):
            erros.append(genero)
        else:
            atualizacao["genero"] = genero.lower()

    if "capa" in dados:
        capa = validar_string(dados["capa"], "Capa")
        if not isinstance(capa, str):
            erros.append(capa)
        else:
            atualizacao["capa"] = capa

    if "idade" in dados:
        idade, erro = validar_idade(dados["idade"])
        if erro:
            erros.append(erro)
        else:
            atualizacao["idade"] = idade

    if erros:
        return erro_resposta(erros)

    SerieService.atualizar(serie, atualizacao)
    return jsonify({"message": "Série atualizada com sucesso."}), 200


# DELETAR SÉRIE
@series_bp.route("/deletar/<int:serie_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def deletar_serie(serie_id):
    serie = SerieService.obter_por_id(serie_id)
    if not serie:
        return erro_resposta(["Série não encontrada."], 404)

    SerieService.deletar(serie)
    return jsonify({"message": "Série deletada com sucesso."}), 200
