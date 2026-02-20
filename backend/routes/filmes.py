from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils.permissions import admin_required

from validators.validators import (
    validar_string,
    validar_idade,
    validar_int_positivo,
    validar_data_iso
)

from utils.http import erro_resposta
from services.filme_service import FilmeService

filmes_bp = Blueprint("filmes", __name__)


# LISTAR FILMES
@filmes_bp.route("", methods=["GET"])
def listar_filmes():
    try:
        filmes = FilmeService.listar(
            titulo=request.args.get("titulo", "").strip() or None,
            genero=request.args.get("genero", "").strip().lower() or None,
            idade_max=request.args.get("idade_max", type=int)
        )
    except ValueError as e:
        return erro_resposta([str(e)])

    return jsonify([
        {
            "id": f.id,
            "titulo": f.titulo,
            "descricao": f.descricao,
            "data_lancamento": f.data_lancamento.isoformat() if f.data_lancamento else None,
            "duracao": f.duracao,
            "idade": f.idade,
            "genero": f.genero,
            "capa": f.capa,
            "nome_arquivo_video": f.nome_arquivo_video
        }
        for f in filmes
    ]), 200


# ADICIONAR FILME 
@filmes_bp.route("/adicionar", methods=["POST"])
@jwt_required()
@admin_required
def adicionar_filme():
    dados = request.get_json() or {}
    erros = []

    titulo = validar_string(dados.get("titulo"), "Título")
    descricao = validar_string(dados.get("descricao"), "Descrição")
    genero = validar_string(dados.get("genero"), "Gênero")
    capa = validar_string(dados.get("capa"), "Capa")
    video = validar_string(dados.get("nome_arquivo_video"), "Arquivo de vídeo")

    duracao = validar_int_positivo(dados.get("duracao"), "Duração")
    idade, erro_idade = validar_idade(dados.get("idade"))
    if "data_lancamento" not in dados:
        erros.append("Data de lançamento é obrigatória.")
    else:
        data_lancamento, erro_data = validar_data_iso(dados.get("data_lancamento"))
        if erro_data or data_lancamento is None:
            erros.append("Data de lançamento inválida.")

    if not isinstance(titulo, str):
        erros.append(titulo)

    if not isinstance(descricao, str):
        erros.append(descricao)

    if not isinstance(genero, str):
        erros.append(genero)

    if not isinstance(capa, str):
        erros.append(capa)

    if not isinstance(video, str):
        erros.append(video)

    if not isinstance(duracao, int):
        erros.append("Duração inválida.")

    if erro_idade:
        erros.append(erro_idade)

    if erro_data:
        erros.append(erro_data)

    if erros:
        return erro_resposta(erros)

    payload = {
        "titulo": titulo,
        "descricao": descricao,
        "genero": genero.lower(),
        "capa": capa,
        "nome_arquivo_video": video,
        "duracao": duracao,
        "idade": idade,
        "data_lancamento": data_lancamento
    }

    try:
        filme = FilmeService.criar(payload)
    except ValueError as e:
        return erro_resposta([str(e)], 409)

    return jsonify({"id": filme.id}), 201


# EDITAR FILME
@filmes_bp.route("/editar/<int:filme_id>", methods=["PUT"])
@jwt_required()
@admin_required
def editar_filme(filme_id):
    filme = FilmeService.obter_por_id(filme_id)
    if not filme:
        return erro_resposta(["Filme não encontrado."], 404)

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

    if "nome_arquivo_video" in dados:
        video = validar_string(dados["nome_arquivo_video"], "Arquivo de vídeo")
        if not isinstance(video, str):
            erros.append(video)
        else:
            atualizacao["nome_arquivo_video"] = video

    if "duracao" in dados:
        duracao = validar_int_positivo(dados["duracao"], "Duração")
        if not isinstance(duracao, int):
            erros.append("Duração inválida.")
        else:
            atualizacao["duracao"] = duracao

    if "idade" in dados:
        idade, erro = validar_idade(dados["idade"])
        if erro:
            erros.append(erro)
        else:
            atualizacao["idade"] = idade

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

    FilmeService.atualizar(filme, atualizacao)
    return jsonify({"message": "Filme atualizado com sucesso."}), 200


# DELETAR FILME
@filmes_bp.route("/deletar/<int:filme_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def deletar_filme(filme_id):
    filme = FilmeService.obter_por_id(filme_id)
    if not filme:
        return erro_resposta(["Filme não encontrado."], 404)

    FilmeService.deletar(filme)
    return jsonify({"message": "Filme deletado com sucesso."}), 200
