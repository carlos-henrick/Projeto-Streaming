import os
from flask import Blueprint, request, Response, current_app
from flask_jwt_extended import jwt_required
from models.tabelas import Filme, Episodio

player_bp = Blueprint("player", __name__)

def get_videos_dir():
    return os.path.join(current_app.root_path, "videos")

def stream_video(path):
    file_size = os.path.getsize(path)
    range_header = request.headers.get("Range")

    if not range_header:
        with open(path, "rb") as f:
            data = f.read()
        return Response(
            data,
            mimetype="video/mp4",
            headers={"Content-Length": str(file_size)}
        )

    bytes_range = range_header.replace("bytes=", "").split("-")
    try:
        start = int(bytes_range[0])
        end = int(bytes_range[1]) if bytes_range[1] else file_size - 1
    except ValueError:
        return Response(status=416)

    if start >= file_size:
        return Response(status=416)

    end = min(end, file_size - 1)
    length = end - start + 1

    with open(path, "rb") as f:
        f.seek(start)
        data = f.read(length)

    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(length)
    }

    return Response(
        data,
        status=206,
        headers=headers,
        mimetype="video/mp4"
    )


@player_bp.route("/<tipo>/<int:midia_id>", methods=["GET"])
@jwt_required()
def player(tipo, midia_id):

    if tipo == "filme":
        midia = Filme.query.get_or_404(midia_id)
    elif tipo == "episodio":
        midia = Episodio.query.get_or_404(midia_id)
    else:
        return {"erro": "Tipo de mídia inválido"}, 400

    filename = midia.nome_arquivo_video
    videos_dir = get_videos_dir()
    path = os.path.join(videos_dir, filename)

    if not os.path.isfile(path):
        return {"erro": "Arquivo não encontrado"}, 404

    return stream_video(path)
