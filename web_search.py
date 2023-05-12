from langchain.utilities import SearxSearchWrapper
from langchain.tools import DuckDuckGoSearchRun
search = DuckDuckGoSearchRun()


def web_search(query: str) -> str:
    return search.run(tool_input=query, verbose=True)



while True:
    print(web_search(input("query: ")))