from flask import (
    Blueprint,
    render_template,
    request,
    send_file,
    flash,
    session,
    redirect,
    url_for,
    send_from_directory,
)
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app.watermark import embed_watermark, extract_watermark
from app.db import insert_file, check_leak, get_user_files, log_activity
from app.utils import login_required
from config import Config

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(Config().UPLOAD_FOLDER, filename)


@main_bp.route("/dashboard")
@login_required
def dashboard():
    # print(session)
    user_files = get_user_files(session["user_id"])
    return render_template("dashboard.html", files=user_files)


@main_bp.route("/upload", methods=["POST"])
@login_required
def upload_file():
    try:
        # Validate file exists in request
        if "file" not in request.files:
            flash("No file selected", "danger")
            return redirect(url_for("main.dashboard"))

        file = request.files["file"]

        # Validate file has a name
        if file.filename == "":
            flash("No file selected", "danger")
            return redirect(url_for("main.dashboard"))

        # Validate file extension
        if not allowed_file(file.filename):
            flash(
                "Invalid file type. Allowed formats: "
                + ", ".join(Config["ALLOWED_EXTENSIONS"]),
                "danger",
            )
            return redirect(url_for("main.dashboard"))

        # Secure and create unique filename
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(Config().UPLOAD_FOLDER, unique_filename)

        # Ensure upload directory exists
        os.makedirs(Config().UPLOAD_FOLDER, exist_ok=True)

        # Save original file
        file.save(file_path)

        # Create watermark and output filename
        watermark = f"HuskTag-Id_{session['user_id']}-User_{session['username']}"
        print(f"Watermark: {watermark}")
        output_filename = f"hushtag_{unique_filename}"
        output_path = os.path.join(Config().UPLOAD_FOLDER, output_filename)

        # Process file with watermark
        embed_watermark(file_path, watermark, output_path)

        # Database operations
        insert_file(
            original_name=unique_filename,
            user_id=session["user_id"],
            watermark=watermark,
            watermarked_name=output_filename,
        )

        # Log activity
        log_activity(
            user_id=session["user_id"],
            activity_type="upload",
            description=f"Uploaded {filename}",
        )

        # Clean up original file after processing
        try:
            os.remove(file_path)
        except OSError:
            pass

        flash("File successfully watermarked and ready for download", "success")
        return send_file(
            output_path,
            as_attachment=True,
            download_name=output_filename,
            mimetype="application/octet-stream",
        )

    except FileNotFoundError:
        flash("Upload directory not found", "danger")
    except PermissionError:
        flash("Permission denied when saving file", "danger")
    except Exception as e:
        flash("An error occurred while processing your file : " + str(e), "danger")

    return redirect(url_for("main.dashboard"))


@main_bp.route("/detect", methods=["POST"])
@login_required
def detect_leak():
    if "leaked_file" not in request.files:
        flash("No file selected", "danger")
        return redirect(url_for("main.dashboard"))

    file = request.files["leaked_file"]
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(file_path)

        try:
            extracted_watermark = extract_watermark(file_path)
            if extracted_watermark:
                leaker = check_leak(extracted_watermark)
                log_activity(
                    session["user_id"], "detect", f"Checked {filename} for leaks"
                )
                return render_template(
                    "result.html",
                    leaker=leaker[0],
                    email=leaker[1],
                    watermark=extracted_watermark,
                )
            flash("No watermark detected", "warning")
        except Exception as e:
            flash("Error detecting watermark", "danger")

    return redirect(url_for("main.dashboard"))


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {
        "png",
        "jpg",
        "jpeg",
        "pdf",
        "docx",
    }
