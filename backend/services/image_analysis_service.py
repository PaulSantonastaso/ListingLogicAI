import asyncio
from typing import List

from chains.image_extraction_chain import extract_property_image
from chains.image_caption_chain import generate_caption_for_image
from models.property_image import PropertyImage


MAX_CONCURRENT_IMAGE_ANALYSIS = 8


async def analyze_single_image_async(
    image_bytes,
    filename,
    api_key,
    semaphore: asyncio.Semaphore,
    image_id=None,
):
    async with semaphore:
        loop = asyncio.get_running_loop()

        return await loop.run_in_executor(
            None,
            extract_property_image,
            image_bytes,
            filename,
            api_key,
            image_id,
        )


async def analyze_property_images(uploaded_images, api_key) -> List[PropertyImage]:
    """
    Analyze multiple uploaded property images with capped concurrency.

    uploaded_images should be a list of tuples:
    [(image_bytes, filename), ...]
    """
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_IMAGE_ANALYSIS)
    tasks = []

    for i, (image_bytes, filename) in enumerate(uploaded_images):
        image_id = f"img_{i+1:03}"

        tasks.append(
            analyze_single_image_async(
                image_bytes=image_bytes,
                filename=filename,
                api_key=api_key,
                semaphore=semaphore,
                image_id=image_id,
            )
        )

    results = await asyncio.gather(*tasks)
    return results


async def _caption_single_image(
    image: PropertyImage,
    api_key: str,
    semaphore: asyncio.Semaphore,
    room_caption_index: int = 1,
    room_caption_total: int = 1,
) -> PropertyImage:
    """Generate and attach a marketing caption to a single PropertyImage."""
    async with semaphore:
        caption = await generate_caption_for_image(
            room_type=image.metadata.room_type,
            visible_features=[f.name for f in image.visible_features],
            quality_score=image.metadata.quality_score,
            marketing_worthy=image.metadata.likely_marketing_worthy,
            api_key=api_key,
            room_caption_index=room_caption_index,
            room_caption_total=room_caption_total,
        )
        image.caption = caption
        return image


async def generate_image_captions(
    images: List[PropertyImage],
    api_key: str,
) -> List[PropertyImage]:
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_IMAGE_ANALYSIS)

    # Count occurrences of each room type to inform caption differentiation
    from collections import Counter
    room_type_counts = Counter(img.metadata.room_type for img in images)
    room_type_seen: Counter = Counter()

    tasks = []
    for image in images:
        room_type = image.metadata.room_type
        room_type_seen[room_type] += 1
        tasks.append(
            _caption_single_image(
                image=image,
                api_key=api_key,
                semaphore=semaphore,
                room_caption_index=room_type_seen[room_type],
                room_caption_total=room_type_counts[room_type],
            )
        )

    return await asyncio.gather(*tasks)


async def analyze_and_caption_property_images(
    uploaded_images,
    api_key: str,
) -> List[PropertyImage]:
    """
    Full pipeline: analyze images then generate marketing captions.

    Step 1 — Vision analysis: extract room type, features, quality score
    Step 2 — Caption generation: write a 15-25 word marketing caption
              per image grounded in detected features

    uploaded_images should be a list of tuples:
    [(image_bytes, filename), ...]

    Returns the fully populated PropertyImage list with captions attached.
    """
    analyzed = await analyze_property_images(uploaded_images, api_key)
    captioned = await generate_image_captions(analyzed, api_key)
    return captioned