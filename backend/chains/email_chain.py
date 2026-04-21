from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from models.property_data import EmailCampaign
from utils.prompt_loader import load_prompt_text


def _format_hero_image_context(image_intelligence) -> str:
    if not image_intelligence or not image_intelligence.hero_image_id:
        return "No hero image available. Ground the email opening in the strongest property feature from the MLS description."

    ranked = image_intelligence.ranked_images
    hero = next(
        (img for img in ranked if img.image_id == image_intelligence.hero_image_id),
        None,
    )

    if not hero:
        return "No hero image available. Ground the email opening in the strongest property feature from the MLS description."

    room = (hero.room_type or "space").replace("_", " ").title()
    features = ", ".join(hero.visible_features[:4]) if hero.visible_features else "notable features"

    return (
        f"Hero image: {hero.filename} — {room}. "
        f"Visible features: {features}. "
        f"This is the highest-scoring image in the set. Use it to anchor the Just Listed opening."
    )


def build_email_chain(api_key: str):
    system_prompt = load_prompt_text("email.txt")

    llm = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview", 
        google_api_key=api_key,
        temperature=0.75, 
    )

    structured_llm = llm.with_structured_output(EmailCampaign)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", (
            "Generate the complete 4-email listing campaign using the following inputs.\n\n"
            "Tone:\n{email_tone}\n\n"
            "MLS Description:\n{mls_summary}\n\n"
            "Visual Summary:\n{visual_summary}\n\n"
            "Listing Headline:\n{headline}\n\n"
            "Hero Image:\n{hero_image_context}"
        ))
    ])

    return prompt | structured_llm