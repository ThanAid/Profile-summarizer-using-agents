from langchain_community.tools.tavily_search import TavilySearchResults
import re


def get_profile_url_tavily(name: str):
    """Searches for Linkedin or Twitter Profile Page URL"""
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res


def extract_urls_with_regex(text):
    """
    Extracts the first URL from a JSON string containing a list of dictionaries using regex.

    Args:
    text (str): A string representing a list of dictionaries.

    Returns:
    str: The first URL extracted from the dictionaries, or None if no URL is found.
    """
    url_pattern = r"https?://[^\s]+"
    match = re.search(url_pattern, text)
    if match:
        return match.group(0)
    return None
