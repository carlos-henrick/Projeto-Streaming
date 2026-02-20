from flask import jsonify

def erro_resposta(erros, status=400):
    return jsonify({"errors": erros}), status
