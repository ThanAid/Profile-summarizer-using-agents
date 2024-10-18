from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers.string import StrOutputParser
from utils.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup

def summarize_with(name: str) -> str:
    linkedin_url = lookup(name)
    linkedin_information = scrape_linkedin_profile(linkedin_url, mock=False)

    summary_template = """
    given the LinkedIn information {information} about a person I want you to create:
    1. a short summary
    2. two interesting facts about the person    
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOllama(model="llama3")

    chain = summary_prompt_template | llm | StrOutputParser()

    res = chain.invoke(input={"information": linkedin_information})

    print(res)

if __name__ == "__main__":
    load_dotenv()
    print("Starting summarization")
    summarize_with("Katerina Dervos")
    