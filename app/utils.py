import imghdr

from PIL import Image
from werkzeug.datastructures import FileStorage


def get_image_format(file: FileStorage) -> str:
    file.seek(0)
    img_format = imghdr.what(file)
    file.seek(0)

    if img_format is None:
        try:
            with Image.open(file) as img:
                img_format = img.format.lower()
        except Exception:
            img_format = "unknown"
        finally:
            file.seek(0)

    format_mapping = {
        "jpeg": "JPEG",
        "jpg": "JPEG",
        "png": "PNG",
        "gif": "GIF",
        "bmp": "BMP",
        "tiff": "TIFF",
    }

    return format_mapping.get(img_format.lower(), "PNG")


def get_image_size(file: FileStorage) -> tuple[int, int]:
    file.seek(0)
    with Image.open(file) as img:
        return img.size


def resize_image(
    file: FileStorage,
    width: int | None,
    height: int | None,
    scale_x: float | None,
    scale_y: float | None,
) -> tuple[Image.Image, str]:
    img = Image.open(file.stream)
    original_format = get_image_format(file)

    if scale_x is not None and scale_y is not None:
        new_width = int(img.width * scale_x)
        new_height = int(img.height * scale_y)
    elif width is not None and height is not None:
        new_width = width
        new_height = height
    else:
        return img, original_format

    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        resized_img = img.convert("RGBA").resize((new_width, new_height), Image.LANCZOS)
    else:
        resized_img = img.convert("RGB").resize((new_width, new_height), Image.LANCZOS)

    return resized_img, original_format
