from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from tools.tools import get_profile_url_tavily, extract_urls_with_regex


load_dotenv()

def lookup(name: str) -> str:
    llm = ChatOllama(model="llama3", temperature=0)
    template = """given the full name {name_of_person} I want you to get me a link to their LinkedIn profile page.
                            Your answer should contain only a URL"""
    prompt_template = PromptTemplate(
        input_variables=["name_of_person"], template=template
    )
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 Linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need to get the Linkedin Page URL",
        ),
        Tool(
            name="Extract Linkedin URL from the search results",
            func=extract_urls_with_regex,
            description="useful for when you need to extract the Linkedin URL from the search results",
        ),
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(
        agent=agent, tools=tools_for_agent, verbose=True, handle_parsing_errors=True
    )

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linked_in_url = result["output"]
    return linked_in_url
