import logging
import os
from pathlib import Path
from flask import current_app, jsonify, request
from werkzeug.utils import secure_filename
from models.upload_model import UploadModel

logger = logging.getLogger(__name__)
EXTENSOES_PERMITIDAS = {"png", "jpg", "jpeg", "gif", "pdf", "txt"}


class UploadController:
    @staticmethod
    def arquivo_permitido(nome_arquivo):
        return "." in nome_arquivo and nome_arquivo.rsplit(".", 1)[1].lower() in EXTENSOES_PERMITIDAS

    @staticmethod
    def upload_file():
        if "file" not in request.files:
            return jsonify({"erro": "Nenhum arquivo enviado. Use o campo 'file'."}), 400
        arquivo = request.files["file"]
        if not arquivo.filename:
            return jsonify({"erro": "Nome do arquivo vazio."}), 400

        nome_arquivo = secure_filename(arquivo.filename)
        if not nome_arquivo:
            return jsonify({"erro": "Nome de arquivo inválido."}), 400
        if not UploadController.arquivo_permitido(nome_arquivo):
            return jsonify({
                "erro": "Tipo de arquivo não permitido.",
                "tipos_permitidos": sorted(EXTENSOES_PERMITIDAS),
            }), 400

        # Mede apenas o conteúdo do arquivo, sem contar o cabeçalho multipart.
        arquivo.stream.seek(0, os.SEEK_END)
        tamanho = arquivo.stream.tell()
        arquivo.stream.seek(0)
        if tamanho > current_app.config["MAX_FILE_SIZE"]:
            return jsonify({"erro": "Arquivo excede o tamanho máximo permitido (30 KB)."}), 413
        if tamanho == 0:
            return jsonify({"erro": "O arquivo está vazio."}), 400

        pasta_upload = Path(current_app.config["UPLOAD_FOLDER"])
        pasta_upload.mkdir(parents=True, exist_ok=True)
        caminho = pasta_upload / nome_arquivo
        if caminho.exists() or UploadModel.find_by_filename(nome_arquivo):
            return jsonify({"erro": "Já existe um arquivo com esse nome. Renomeie-o e tente novamente."}), 409

        try:
            arquivo.save(str(caminho))
            salvo_no_banco = UploadModel.save_file(nome_arquivo, str(caminho.resolve()))
            if not salvo_no_banco:
                caminho.unlink(missing_ok=True)
                return jsonify({"erro": "Já existe um registro com esse nome."}), 409
        except Exception:
            caminho.unlink(missing_ok=True)
            logger.exception("Erro ao salvar upload")
            return jsonify({"erro": "Não foi possível salvar o arquivo."}), 500

        logger.info("Upload concluído: %s | IP: %s", nome_arquivo, request.remote_addr)
        return jsonify({
            "mensagem": "Arquivo salvo com sucesso!",
            "arquivo": nome_arquivo,
            "tamanho_bytes": tamanho,
            "download": f"/downloads/download/{nome_arquivo}",
        }), 201
