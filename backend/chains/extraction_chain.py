from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from models.property_data import PropertyDetails
from utils.prompt_loader import load_prompt_text


def build_extraction_chain(api_key: str):
    system_prompt = load_prompt_text("extraction.txt")

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite-preview",
        google_api_key=api_key,
        temperature=0.2,
    )

    structured_llm = llm.with_structured_output(PropertyDetails)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "Here are the raw agent notes:\n\n{raw_notes}")
    ])

    return prompt | structured_llm