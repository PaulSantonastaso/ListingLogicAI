from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from models.property_data import ListingDescriptionOutput
from utils.prompt_loader import load_prompt_text


def build_listing_description_chain(api_key: str):
    system_prompt = load_prompt_text("mls_writer.txt")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.7,
    )

    structured_llm = llm.with_structured_output(ListingDescriptionOutput)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", (
            "Generate an MLS description using the following inputs.\n\n"
            "Property Details:\n{property_details}\n\n"
            "Visual Summary:\n{visual_summary}"
        ))
    ])

    return prompt | structured_llm