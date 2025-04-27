from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app.watermark import embed_watermark
from app.db import insert_file
from config import Config

api_bp = Blueprint("api", __name__)


@api_bp.route("/watermark", methods=["POST"])
def api_watermark():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    user_id = request.form.get("user_id", "anonymous")

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(Config.UPLOAD_FOLDER, unique_filename)
        file.save(file_path)

        watermark = f"User-{user_id}"
        output_filename = f"husktag_{unique_filename}"
        output_path = os.path.join(Config.UPLOAD_FOLDER, output_filename)

        try:
            embed_watermark(file_path, watermark, output_path)
            insert_file(unique_filename, user_id, watermark, output_filename)
            return send_file(output_path, as_attachment=True)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Invalid file type"}), 400


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {
        "png",
        "jpg",
        "jpeg",
        "pdf",
        "docx",
    }
