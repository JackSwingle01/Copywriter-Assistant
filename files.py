import os
from langchain.document_loaders import DirectoryLoader
from langchain.docstore.document import Document

def get_text_docs(input_dir: str) -> list[Document]:
    print("Loading documents...")
    loader = DirectoryLoader(input_dir, glob='**/*.txt', show_progress=True)
    documents = loader.load()

    return documents

def move_files(input_dir: str, output_dir: str = './data/processed/') -> None:

    files = os.listdir(input_dir)
    for f in files:
        os.rename(input_dir + f, output_dir + f)