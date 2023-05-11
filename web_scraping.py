from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from langchain.docstore.document import Document
from docs import make_doc_with_source
from wiki import get_wiki_page

def gather_links_from_url(url: str) -> dict[str, str]:
    """ 
    url: str - the url to gather links from
    Returns a dict of links and their text
    Gets all the links found on a given web page and their text
    """
    # based on https://pythonprogramminglanguage.com/get-links-from-webpage/

    #check if url is valid
    try:
        req = Request(url)
        html_page = urlopen(req)
    except:
        return []

    soup = BeautifulSoup(html_page, "lxml")

    links = dict()
    for link in soup.findAll('a'):
        href = link.get('href').strip()
        text = link.getText().strip()
        if link.get('href') is not None:
            links[href] = text

    return links


def gather_links_from_urls(urls: list[str]) -> dict[str, str]:
    links = dict()
    for url in urls:
        links.update(gather_links_from_url(url))
    return links


def get_wiki_as_doc(page_name: str) -> Document:

    wiki_page = get_wiki_page(page_name)
    if wiki_page is None:
        return None

    doc = make_doc_with_source(
        wiki_page.content, f"{wiki_page.title} Wikipedia Page")
    return doc


def get_doc_from_webpage(url: str, page_name=None) -> Document:

    # get the content of the webpage
    try:
        print(f"Getting content from {url}")
        req = Request(url)
        print("req successful")
        html_page = urlopen(req)
        print("html_page successful")
    except:
        return None

    soup = BeautifulSoup(html_page, "lxml")
    paragraphs = soup.findAll("p")
    text = ""
    for p in paragraphs:
        if p.getText() != "":
            text += p.getText() + "\n"
    
    if text is None:
        print("No text found on page")
        return None
    if page_name is None:
        page_name = url
    doc = make_doc_with_source(text, page_name)

    return doc

