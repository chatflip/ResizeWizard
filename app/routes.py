from __future__ import annotations

import io
from typing import cast

from flask import (
    Blueprint,
    Response,
    make_response,
    render_template,
    request,
    send_file,
)
from werkzeug.datastructures import FileStorage

from app.utils import resize_image

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def index() -> Response:
    if request.method == "POST":
        if "file" not in request.files:
            response = make_response("No file part")
            response.status_code = 400
            return response

        file: FileStorage = request.files["file"]

        if file.filename == "":
            response = make_response("No selected file")
            response.status_code = 400
            return response

        if file:
            width = int(request.form["width"])
            height = int(request.form["height"])

            resized_img = resize_image(file, width, height)

            img_io = io.BytesIO()
            resized_img.save(img_io, "JPEG")
            img_io.seek(0)

            return cast(
                Response,
                send_file(
                    img_io,
                    mimetype="image/jpeg",
                    as_attachment=True,
                    download_name="resized_image.jpg",
                ),
            )

    return make_response(render_template("index.html"))
