import base64
from ctypes import cast
import mimetypes
from uuid import uuid4

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from models.property_image import PropertyImage


SYSTEM_INSTRUCTIONS = """
You are a conservative real estate image analyst.

Your job is to analyze ONE uploaded property photo and return structured data.

Rules:
1. Only describe what is clearly visible in the image.
2. Do not invent amenities, materials, finishes, dimensions, or luxury claims unless visually obvious.
3. Use neutral, factual wording.
4. Visible features should be short noun phrases, such as:
   - stainless steel appliances
   - kitchen island
   - double vanity
   - fenced backyard
   - large windows
5. If something is ambiguous, either omit it or lower confidence.
6. Set is_interior and is_exterior conservatively.
7. quality_score should estimate how useful the image is for listing marketing:
   - 0.0 = poor
   - 1.0 = excellent
8. likely_marketing_worthy should be true only if the image is reasonably clear and useful.
9. The description should be 1 concise sentence, factual and non-salesy.
10. Preserve the provided image_id and filename exactly.
11. Return at most 6 visible features.
12. Prioritize features that are useful in real estate marketing, such as:
   - updated finishes
   - kitchen island
   - stainless steel appliances
   - double vanity
   - covered patio
   - fenced backyard
   - large windows
   - pool
   - garage
13. Do not include small movable objects or minor appliances unless they are clearly important to the space.
14. Avoid overly specific low-value details such as stools, microwave color, decor items, or small accessories.
"""


def _guess_mime_type(filename: str) -> str:
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or "image/jpeg"


def _encode_image_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")


def build_image_extraction_model(api_key: str, model_name: str = "gemini-2.5-flash"):
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0,
        google_api_key=api_key
    )


def extract_property_image(
    image_bytes: bytes,
    filename: str,
    api_key: str,
    image_id: str | None = None,
    model_name: str = "gemini-2.5-flash",
) -> PropertyImage:
    """
    Analyze one uploaded image and return a structured PropertyImage object.
    """

    if not image_id:
        image_id = f"img_{uuid4().hex[:12]}"

    mime_type = _guess_mime_type(filename)
    image_b64 = _encode_image_to_base64(image_bytes)

    llm = build_image_extraction_model(api_key, model_name=model_name)
    structured_llm = llm.with_structured_output(PropertyImage)

    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": f"""
{SYSTEM_INSTRUCTIONS}

Provided metadata:
- image_id: {image_id}
- filename: {filename}

Return a PropertyImage object for this single uploaded property photo.
""".strip(),
            },
            {
                "type": "image_url",
                "image_url": f"data:{mime_type};base64,{image_b64}",
            },
        ]
    )

    raw_result = structured_llm.invoke([message])
    result = PropertyImage.model_validate(raw_result)

    for feature in result.visible_features:
        if feature.source == "vision":
            feature.source = "image"

    # Defensive normalization in case the model drifts
    result.image_id = image_id
    result.filename = filename
    result.metadata.image_id = image_id
    result.metadata.filename = filename

    return result