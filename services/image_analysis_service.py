import asyncio
from typing import List

from chains.image_extraction_chain import extract_property_image
from models.property_image import PropertyImage


MAX_CONCURRENT_IMAGE_ANALYSIS = 4


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