from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from models.property_data import SocialPostOutput
from utils.prompt_loader import load_prompt_text


def build_social_post_chain(api_key: str):
    system_prompt = load_prompt_text("social_media.txt")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=api_key,
        temperature=0.8,
    )

    structured_llm = llm.with_structured_output(SocialPostOutput)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", (
            "Generate one platform-specific social media post using the following inputs.\n\n"
            "Property Details:\n{property_details}\n\n"
            "MLS Description:\n{mls_summary}\n\n"
            "Visual Summary:\n{visual_summary}\n\n"
            "Platform:\n{platform}\n\n"
            "Slot Name:\n{slot_name}\n\n"
            "Selected Image ID:\n{image_id}\n\n"
            "Selected Image Filename:\n{image_filename}\n\n"
            "Recommended Aspect Ratio:\n{recommended_aspect_ratio}\n\n"
            "Crop Guidance:\n{crop_guidance}\n\n"
            "Room Type:\n{room_type}\n\n"
            "Visible Features:\n{visible_features}"
        ))
    ])

    return prompt | structured_llm