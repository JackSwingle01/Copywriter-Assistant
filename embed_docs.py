import os
from langchain.vectorstores import Chroma

from vector_db import make_chroma_db, clear_existing_db, chunk_docs
from files import get_text_docs, move_files

from config import OPENAI_API_KEY, VECTORSTORE_DIRECTORY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY




def make_chroma_from_dir(src_dir: str, db_persist_dir: str = VECTORSTORE_DIRECTORY, chunk_size: int = 1000) -> Chroma:

    # get docs from directory
    documents = get_text_docs(src_dir)
    # chunk docs
    texts = chunk_docs(documents, chunk_size=chunk_size, overlap=int(chunk_size/10))
    # make db
    db = make_chroma_db(texts, persist_dir=db_persist_dir)
    # persist db
    db.persist()

    return db



    


if __name__ == "__main__":
    dir = input(
        "Enter source directory for documents (enter for default: ./data/to_process/): ")
    if dir != '':
        input_dir = dir
    else:
        input_dir = './data/to_process/'

    choice = input("Would you like to clear the existing database? (y/n): ")
    if choice == 'y':
        clear_existing_db()

    make_chroma_from_dir(
        input_dir, db_persist_dir=VECTORSTORE_DIRECTORY, chunk_size=500)

    choice = input(
        "Would you like to move the processed documents to a new directory? (y/n): ")
    if choice == 'y':
        output = input(
            "Enter output directory for processed documents (enter for default: ./data/processed/): ")
        if output != '':
            output_dir = output
        else:
            output_dir = './data/processed/'

        move_files(input_dir, output_dir=output_dir)
