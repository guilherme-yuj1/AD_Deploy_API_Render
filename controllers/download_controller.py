from pathlib import Path
from flask import current_app, jsonify, send_file
from models.download_model import DownloadModel


class DownloadController:
    @staticmethod
    def download_file(filename):
        registro = DownloadModel.find_by_filename(filename)
        if registro is None:
            return jsonify({"erro": "Arquivo não encontrado."}), 404

        caminho = Path(registro["filepath"]).resolve()
        pasta_upload = Path(current_app.config["UPLOAD_FOLDER"]).resolve()
        try:
            caminho.relative_to(pasta_upload)
        except ValueError:
            return jsonify({"erro": "Caminho de arquivo inválido."}), 404
        if not caminho.is_file():
            return jsonify({"erro": "O arquivo não está disponível no armazenamento."}), 404
        return send_file(caminho, as_attachment=True, download_name=registro["filename"])
