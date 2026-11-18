import os
from pathlib import Path
from flask import Flask, jsonify
from database.db import init_db
from routes.upload_route import upload_bp
from routes.download_route import download_bp


def create_app():
    app = Flask(__name__)
    project_dir = Path(__file__).resolve().parent
    upload_folder = Path(os.getenv("UPLOAD_FOLDER", project_dir / "uploads")).resolve()
    database_path = Path(os.getenv("DATABASE_PATH", project_dir / "instance" / "database.db")).resolve()
    upload_folder.mkdir(parents=True, exist_ok=True)
    database_path.parent.mkdir(parents=True, exist_ok=True)
    app.config.update(
        UPLOAD_FOLDER=str(upload_folder),
        DATABASE_PATH=str(database_path),
        MAX_CONTENT_LENGTH=1024 * 1024,
        MAX_FILE_SIZE=30 * 1024,
    )
    init_db(app.config["DATABASE_PATH"])
    app.register_blueprint(upload_bp, url_prefix="/uploads")
    app.register_blueprint(download_bp, url_prefix="/downloads")

    @app.get("/")
    def health_check():
        return jsonify({
            "status": "online",
            "mensagem": "API de Upload e Download funcionando!",
            "endpoints": {
                "upload": "POST /uploads/upload (campo multipart: file)",
                "download": "GET /downloads/download/<filename>",
            },
        }), 200

    @app.errorhandler(413)
    def request_too_large(_error):
        return jsonify({"erro": "Requisição muito grande. O arquivo deve respeitar o limite de 30 KB."}), 413

    return app


app = create_app()

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=debug)
