from PIL import Image
from werkzeug.datastructures import FileStorage


def resize_image(file: FileStorage, width: int, height: int) -> Image:
    img = Image.open(file.stream)
    return img.resize((width, height))
