from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from models.property_data import SocialPostOutput
from utils.prompt_loader import load_prompt_text


def build_social_post_chain(api_key: str):
    system_prompt = load_prompt_text("listing_system_prompt.txt")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.8,
    )

    structured_llm = llm.with_structured_output(SocialPostOutput)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", (
            "Generate a social media post using the following property data and MLS description.\n\n"
            "Property Details:\n{property_details}\n\n"
            "MLS Description:\n{mls_summary}"
        ))
    ])

    return prompt | structured_llm