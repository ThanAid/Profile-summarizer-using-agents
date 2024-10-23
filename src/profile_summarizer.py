from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_ollama import ChatOllama
from utils.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup
from utils.output_parsers import summary_parser, Summary
from typing import Tuple


def summarize_with(name: str) -> Tuple[Summary, str]:
    linkedin_url = lookup(name)
    linkedin_information = scrape_linkedin_profile(linkedin_url, mock=False)

    summary_template = """
    given the LinkedIn information {information} about a person I want you to create:
    1. a short summary
    2. two interesting facts about the person
    \n{format_instructions}    
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

    llm = ChatOllama(model="llama3")

    chain = summary_prompt_template | llm | summary_parser

    res = chain.invoke(input={"information": linkedin_information})

    return res, linkedin_information.get("profile_pic_url")


if __name__ == "__main__":
    load_dotenv()
    print("Starting summarization")
    summarize_with("Thanos Aidinis")
