import io
from PIL import Image, ImageEnhance, ImageOps


def enhance_listing_photo(
    image_bytes: bytes,
    max_size: tuple[int, int] = (2000, 2000),
    output_format: str = "JPEG",
    quality: int = 95,
) -> bytes:
    """
    Apply lightweight professional-style enhancement to a listing photo.
    """

    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Normalize orientation from phone metadata
    img = ImageOps.exif_transpose(img)

    # Resize while preserving aspect ratio
    img.thumbnail(max_size)

    # Mild enhancement values to avoid overprocessing
    img = ImageEnhance.Brightness(img).enhance(1.08)
    img = ImageEnhance.Contrast(img).enhance(1.12)
    img = ImageEnhance.Color(img).enhance(1.04)
    img = ImageEnhance.Sharpness(img).enhance(1.10)

    output = io.BytesIO()
    img.save(output, format=output_format, quality=quality, optimize=True)
    return output.getvalue()


def enhance_listing_photos(uploaded_images):
    """
    uploaded_images: list of tuples [(image_bytes, filename), ...]
    returns: list of tuples [(enhanced_bytes, filename), ...]
    """
    enhanced = []

    for image_bytes, filename in uploaded_images:
        enhanced_bytes = enhance_listing_photo(image_bytes)
        enhanced.append((enhanced_bytes, filename))

    return enhanced