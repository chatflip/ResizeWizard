import io

from flask import (
    Blueprint,
    Response,
    jsonify,
    make_response,
    render_template,
    request,
    send_file,
)
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.utils import get_image_size, resize_image

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def index() -> Response:
    return make_response(render_template("index.html"))


@main.route("/get_image_size", methods=["POST"])
def get_image_size_route() -> Response:
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file: FileStorage = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file:
        width, height = get_image_size(file)
        return jsonify({"width": width, "height": height})


@main.route("/resize", methods=["POST"])
def resize() -> Response:
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file: FileStorage = request.files["file"]
    resize_type = request.form.get("resize_type")

    if resize_type == "pixel":
        width = int(request.form.get("width")) if request.form.get("width") else None
        height = int(request.form.get("height")) if request.form.get("height") else None
        scale_x, scale_y = None, None
    elif resize_type == "scale":
        scale_x = (
            float(request.form.get("scale_x")) if request.form.get("scale_x") else None
        )
        scale_y = (
            float(request.form.get("scale_y")) if request.form.get("scale_y") else None
        )
        width, height = None, None
    else:
        return jsonify({"error": "Invalid resize type"}), 400

    resized_img, original_format = resize_image(file, width, height, scale_x, scale_y)

    img_io = io.BytesIO()

    save_kwargs = {}
    if original_format == "JPEG":
        save_kwargs["quality"] = 95
        save_kwargs["optimize"] = True

    resized_img.save(img_io, format=original_format, **save_kwargs)
    img_io.seek(0)

    return send_file(
        img_io,
        mimetype=f"image/{original_format.lower()}",
        as_attachment=True,
        download_name=f"resized_{secure_filename(file.filename)}",
    )
