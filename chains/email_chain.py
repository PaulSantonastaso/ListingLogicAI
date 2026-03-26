from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from models.property_data import EmailCampaign
from utils.prompt_loader import load_prompt_text


def build_email_chain(api_key: str):
    system_prompt = load_prompt_text("email.txt")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        google_api_key=api_key,
        temperature=0.75, 
    )

    structured_llm = llm.with_structured_output(EmailCampaign)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", (
            "Generate a lead generation email using the following inputs.\n\n"
            "Tone:\n{email_tone}\n\n"
            "MLS Description:\n{mls_summary}\n\n"
            "Visual Summary:\n{visual_summary}"
        ))
    ])

    return prompt | structured_llm