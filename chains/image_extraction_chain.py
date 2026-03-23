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
"""


def _guess_mime_type(filename: str) -> str:
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or "image/jpeg"


def _encode_image_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")


def build_image_extraction_model(model_name: str = "gemini-2.5-flash") -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0,
    )


def extract_property_image(
    image_bytes: bytes,
    filename: str,
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

    llm = build_image_extraction_model(model_name=model_name)
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

    # Defensive normalization in case the model drifts
    result.image_id = image_id
    result.filename = filename
    result.metadata.image_id = image_id
    result.metadata.filename = filename

    return result