import io
from typing import List, Tuple

import cv2
import numpy as np
from PIL import Image, ImageOps


def _read_image(image_bytes: bytes) -> np.ndarray:
    pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    pil_img = ImageOps.exif_transpose(pil_img)
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)


def _encode_jpeg(image_bgr: np.ndarray, quality: int = 95) -> bytes:
    success, encoded = cv2.imencode(
        ".jpg",
        image_bgr,
        [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    )
    if not success:
        raise ValueError("Failed to encode enhanced image to JPEG.")
    return encoded.tobytes()


def _resize_preserving_aspect(
    image_bgr: np.ndarray,
    max_dim: int = 1800
) -> np.ndarray:
    h, w = image_bgr.shape[:2]
    longest = max(h, w)

    if longest <= max_dim:
        return image_bgr

    scale = max_dim / float(longest)
    new_w = int(w * scale)
    new_h = int(h * scale)

    return cv2.resize(image_bgr, (new_w, new_h), interpolation=cv2.INTER_AREA)


def _gray_world_white_balance(image_bgr: np.ndarray) -> np.ndarray:
    img = image_bgr.astype(np.float32)
    b, g, r = cv2.split(img)

    b_mean = np.mean(b)
    g_mean = np.mean(g)
    r_mean = np.mean(r)
    avg = (b_mean + g_mean + r_mean) / 3.0

    b *= avg / max(b_mean, 1e-6)
    g *= avg / max(g_mean, 1e-6)
    r *= avg / max(r_mean, 1e-6)

    balanced = cv2.merge([b, g, r])
    return np.clip(balanced, 0, 255).astype(np.uint8)


def _apply_clahe(image_bgr: np.ndarray) -> np.ndarray:
    lab = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=1.6, tileGridSize=(8, 8))
    l2 = clahe.apply(l)

    merged = cv2.merge([l2, a, b])
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)


def _mild_denoise(image_bgr: np.ndarray) -> np.ndarray:
    return cv2.fastNlMeansDenoisingColored(
        image_bgr,
        None,
        3,   # h
        3,   # hColor
        7,   # templateWindowSize
        21   # searchWindowSize
    )


def _clarity_boost(image_bgr: np.ndarray) -> np.ndarray:
    blurred = cv2.GaussianBlur(image_bgr, (0, 0), sigmaX=3)
    clarity = cv2.addWeighted(image_bgr, 1.12, blurred, -0.08, 0)
    return np.clip(clarity, 0, 255).astype(np.uint8)


def _edge_aware_sharpen(image_bgr):
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 60, 120)
    edges = cv2.medianBlur(edges, 3)

    blurred = cv2.GaussianBlur(image_bgr, (0,0), 1.2)
    sharpened = cv2.addWeighted(image_bgr, 1.13, blurred, -0.10, 0)

    kernel = np.ones((3,3), np.uint8)
    mask = cv2.dilate(edges, kernel)
    mask = cv2.GaussianBlur(mask, (9,9), 0)

    mask = mask.astype(np.float32) / 255.0
    mask = mask[:,:,None]

    result = image_bgr*(1-mask) + sharpened*mask
    return np.clip(result, 0, 255).astype(np.uint8)


def _auto_straighten(image_bgr: np.ndarray, max_rotation_degrees: float = 3.0) -> np.ndarray:
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=80,
        minLineLength=max(image_bgr.shape[:2]) // 4,
        maxLineGap=20
    )

    if lines is None:
        return image_bgr

    angles = []
    for line in lines[:, 0]:
        x1, y1, x2, y2 = line
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))

        # focus on near-horizontal lines for rotation estimate
        if -15 <= angle <= 15:
            angles.append(angle)

    if not angles:
        return image_bgr

    median_angle = float(np.median(angles))

    if abs(median_angle) < 0.2 or abs(median_angle) > max_rotation_degrees:
        return image_bgr

    h, w = image_bgr.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, median_angle, 1.0)

    return cv2.warpAffine(
        image_bgr,
        matrix,
        (w, h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REPLICATE
    )


def _vertical_perspective_correction(image_bgr: np.ndarray) -> np.ndarray:
    """
    Light heuristic correction for converging verticals.
    Keeps it conservative to avoid artifacts.
    """
    h, w = image_bgr.shape[:2]
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=100,
        minLineLength=h // 4,
        maxLineGap=20
    )

    if lines is None:
        return image_bgr

    vertical_angles = []
    for line in lines[:, 0]:
        x1, y1, x2, y2 = line
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        # near-vertical lines
        if 75 <= abs(angle) <= 105:
            vertical_angles.append(angle)

    if not vertical_angles:
        return image_bgr

    # estimate how tilted verticals are away from perfect 90
    normalized = []
    for a in vertical_angles:
        if a < 0:
            a += 180
        normalized.append(a)

    median_angle = float(np.median(normalized))
    deviation = median_angle - 90.0

    if abs(deviation) < 1.0 or abs(deviation) > 8.0:
        return image_bgr

    # very light keystone-style correction
    shift = int(w * min(abs(deviation) / 100.0, 0.06))
    shift = max(1, shift)

    if deviation > 0:
        src = np.array([
            [shift, 0],
            [w - shift, 0],
            [0, h],
            [w, h]
        ], dtype=np.float32)
    else:
        src = np.array([
            [0, 0],
            [w, 0],
            [shift, h],
            [w - shift, h]
        ], dtype=np.float32)

    dst = np.array([
        [0, 0],
        [w, 0],
        [0, h],
        [w, h]
    ], dtype=np.float32)

    matrix = cv2.getPerspectiveTransform(src, dst)
    corrected = cv2.warpPerspective(
        image_bgr,
        matrix,
        (w, h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REPLICATE
    )

    return corrected


def enhance_listing_photo(
    image_bytes: bytes,
    max_dim: int = 1800,
    jpeg_quality: int = 95,
) -> bytes:
    image = _read_image(image_bytes)
    image = _resize_preserving_aspect(image, max_dim=max_dim)

    # Geometry first
    image = _auto_straighten(image)
    image = _vertical_perspective_correction(image)

    # Tone / color
    image = _gray_world_white_balance(image)
    image = _window_protect(image)
    image = _shadow_lift(image)
    image = _apply_clahe(image)

    # Detail cleanup
    image = _mild_denoise(image)
    image = _clarity_boost(image)
    image = _edge_aware_sharpen(image)
    image = cv2.bilateralFilter(image, 5, 20, 20)

    return _encode_jpeg(image, quality=jpeg_quality)


def enhance_listing_photos(
    uploaded_images: List[Tuple[bytes, str]]
) -> List[Tuple[bytes, str]]:
    enhanced = []

    for image_bytes, filename in uploaded_images:
        enhanced_bytes = enhance_listing_photo(image_bytes)
        enhanced.append((enhanced_bytes, filename))

    return enhanced

def _shadow_lift(image_bgr):
    gamma = 0.9
    inv_gamma = 1.0 / gamma
    table = np.array([(i / 255.0) ** inv_gamma * 255 for i in range(256)]).astype("uint8")
    return cv2.LUT(image_bgr, table)

def _window_protect(image_bgr):
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    # detect very bright areas (likely windows)
    _, mask = cv2.threshold(gray, 235, 255, cv2.THRESH_BINARY)

    mask = cv2.GaussianBlur(mask, (21,21), 0)
    mask = mask.astype(np.float32) / 255.0
    mask = mask[:,:,None]

    # slightly darken highlights
    highlight_reduce = cv2.addWeighted(image_bgr, 0.9, image_bgr, 0, 0)

    result = image_bgr*(1-mask) + highlight_reduce*mask
    return result.astype(np.uint8)