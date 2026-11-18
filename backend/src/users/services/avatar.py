from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from PIL import Image, ImageOps, UnidentifiedImageError


MAX_FILE_SIZE = 5 * 1024 * 1024
MAX_DIMENSION = 256
MAX_PIXELS = 20_000_000
ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}


def prepare_avatar(file):
    if file.size > MAX_FILE_SIZE:
        raise ValidationError("Максимальный размер изображения 5 МБ.")

    try:
        with Image.open(file) as image:
            if image.format not in ALLOWED_FORMATS:
                raise ValidationError(
                    "Поддерживаются только JPEG, PNG и WebP.")

            if image.width * image.height > MAX_PIXELS:
                raise ValidationError(
                    "Слишком большое разрешение изображения.")

            image = ImageOps.exif_transpose(image)
            image = image.convert("RGBA")

            image.thumbnail(
                (MAX_DIMENSION, MAX_DIMENSION),
                Image.Resampling.LANCZOS,
            )

            output = BytesIO()
            image.save(output, format="WEBP", quality=85)

    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise ValidationError("Некорректное изображение.") from exc

    return ContentFile(output.getvalue(), name="avatar.webp")
