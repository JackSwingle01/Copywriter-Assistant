from files import get_text_docs
from web_scraping import gather_links_from_urls, get_wiki_as_doc, get_doc_from_webpage
from docs import find_all_urls_in_docs, remove_duplicate_content_docs, chunk_docs
from vector_db import VectorDB


def gather_info(subject: str, dir: str = './data/to_process/') -> None:
    """
    Gather information about a subject from a directory of documents and the web.
    Stores it in the Chroma DB at the specified directory.
    """

    docs = get_text_docs(dir)

    print("Extracting urls from documents...")
    links = dict()
    urls = find_all_urls_in_docs(docs)
    for url in urls:
        links[url] = url



    print("Extracting links from webpages...")
    links.update(gather_links_from_urls(urls))

    # print(links)

    print("Extracting content from links...")
    for url in links.keys():
        source_title = links[url]
        doc = get_doc_from_webpage(url, source_title)
        if doc is not None:
            docs.append(doc)
            print(f"Added {source_title} to documents.")

    print(f"Found {len(docs)} documents.")
    print("Removing duplicates...")
    docs = remove_duplicate_content_docs(docs)

    print("Getting Wikipedia page...")
    while True:
        wiki_doc = get_wiki_as_doc(subject)
        if wiki_doc is None:
            print("Could not find Wikipedia page, try again.")
            subject = input("Enter wiki page title: ")
        else:
            docs.append(wiki_doc)
            break

    print("Chunking documents...")
    docs = chunk_docs(docs, 1200, 200)
    print(f"Found {len(docs)} documents.")
    print(
        f"Larges document is {max([len(doc.page_content) for doc in docs])} characters long.")

    print("Creating database...")
    db = VectorDB()
    print("Clearing existing database...")
    db.clear_all_docs()
    print("Adding documents to database...")
    db.add_documents(docs)

    print("Done!")


if __name__ == "__main__":

    dir = input("Enter directory to get docs from: ")
    if dir == '':
        dir = './data/to_process/'

    institution_name = input("Enter institution name: ")

    gather_info(institution_name, dir)
