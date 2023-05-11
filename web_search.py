from langchain.tools import DuckDuckGoSearchRun
search = DuckDuckGoSearchRun()

def web_search(query: str) -> str:
    return search.run(query, verbose=True)
