from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from models.video_script import VideoScriptSuite
from utils.prompt_loader import load_prompt_text


def _format_shot_list(shot_plan: dict) -> str:
    """
    Format the per-platform shot plan into a readable string
    for injection into the video script prompt.
    """
    lines = []

    for platform, shots in shot_plan.items():
        platform_label = platform.replace("_", " ").title()
        lines.append(f"[ {platform_label} ]")

        for shot in shots:
            filename_note = f" — {shot.image_filename}" if shot.image_filename else " — no image"
            room_note = f" ({shot.room_type.replace('_', ' ').title()})" if shot.room_type else ""
            features_note = (
                f" | Features: {', '.join(shot.visible_features)}"
                if shot.visible_features
                else ""
            )
            lines.append(
                f"  Shot {shot.order}{filename_note}{room_note}{features_note}"
            )
            lines.append(f"  Direction: {shot.direction}")

        lines.append("")

    return "\n".join(lines).strip()


def _format_hero_image_context(image_intelligence) -> str:
    """
    Build a concise hero image context string for the prompt.
    Returns a fallback message if no image intelligence is available.
    """
    if not image_intelligence or not image_intelligence.hero_image_id:
        return "No hero image available. Ground the opening in the strongest property feature from the MLS description."

    ranked = image_intelligence.ranked_images
    hero = next(
        (img for img in ranked if img.image_id == image_intelligence.hero_image_id),
        None,
    )

    if not hero:
        return "No hero image available. Ground the opening in the strongest property feature from the MLS description."

    room = (hero.room_type or "space").replace("_", " ").title()
    features = ", ".join(hero.visible_features[:4]) if hero.visible_features else "notable features"

    return (
        f"Hero image: {hero.filename} — {room}. "
        f"Visible features: {features}. "
        f"This is the highest-scoring image in the set. Lead with it where possible."
    )


def build_video_script_chain(api_key: str):
    system_prompt = load_prompt_text("video_scripts.txt")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.75,
    )

    structured_llm = llm.with_structured_output(VideoScriptSuite)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", (
            "Generate the complete 3-platform video script suite using the following inputs.\n\n"
            "Property Details:\n{property_details}\n\n"
            "MLS Description:\n{mls_summary}\n\n"
            "Visual Summary:\n{visual_summary}\n\n"
            "Shot List:\n{shot_list}\n\n"
            "Hero Image:\n{hero_image_context}"
        ))
    ])

    return prompt | structured_llm