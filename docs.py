from langchain.docstore.document import Document
from custom_chains import make_findURLs_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter


def format_url(url: str) -> str:
    """
    url: str - the url to format
    Returns a formatted url
    """
    url = url.strip()
    url = url.strip("[]")
    url = url.strip("'")

    if url == "NONE" or url == "" or url == "None":
        return None

    if url.startswith("http://") or url.startswith("https://"):
        return url
    else:
        return "http://" + url


def find_all_urls_in_docs(docs: list[Document]) -> list[str]:
    """
    db: Chroma - the database to search
    Returns a list of all the links found in the database
    """
    chain = make_findURLs_chain(verbose=True)

    urls = []
    for doc in docs:
        found_urls = chain.run(doc).split(",")
        found_urls = [format_url(url) for url in found_urls]
        for url in found_urls:
            if url is not None and url not in urls:
                urls.append(url)

    return urls


def make_doc_with_source(text: str, source: str) -> Document:

    page_content = text
    metadata = {"source": source}
    doc = Document(page_content=page_content, metadata=metadata)

    return doc


def chunk_docs(docs: list[Document], chunk_size: int = 400, chunk_overlap: int = 40) -> list[Document]:

    import tiktoken
    tokenizer = tiktoken.get_encoding("cl100k_base")

    def tiktoken_len(text: str) -> int:
        return len(tokenizer.encode(text,disallowed_special=()))

    all_chunks = []
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", "!", ",", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=tiktoken_len
    )
    chunks = []
    for doc in docs:
        chunks = text_splitter.split_documents([doc])
        n = 0
        for chunk in chunks:
            chunk.metadata["chunk_number"] = n
            n += 1
        all_chunks += chunks

    return all_chunks


def remove_duplicate_content_docs(docs: list[Document]) -> list[Document]:
    
    uniques = []
    seen_content = set()
    for doc in docs:
        if doc.page_content is None:
            print("ERROR - doc has no content", doc.metadata["source"])
        if doc.page_content not in seen_content:
            print("adding", doc.metadata["source"])
            uniques.append(doc)
            seen_content.add(doc.page_content)
    
    return uniques
