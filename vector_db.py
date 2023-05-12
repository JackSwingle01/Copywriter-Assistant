import os
import random

from langchain import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA

import chromadb
from chromadb.config import Settings
from chromadb.api.local import LocalAPI
from chromadb.api.models.Collection import Collection

from config import OPENAI_API_KEY, VECTORSTORE_DIRECTORY, CHAT_MODEL
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
EMBEDDINGS_API = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)


class VectorDB:

    def __init__(self, directory: str = VECTORSTORE_DIRECTORY, embedding_function=EMBEDDINGS_API) -> None:

        self.directory = directory
        self.embedding_function = embedding_function
        self._client: LocalAPI = self._make_client()
        self.collection: Collection = self._load_collection()
        self.langchain_wrapper = self.get_as_langchain_wrapper()

    def _make_client(self) -> LocalAPI:

        return chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=self.directory
        ))

    def _load_collection(self, collection_name: str = "default") -> Collection:
        return self._client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function.embed_documents
        )

    def _create_new_collection(self, collection_name: str = "default") -> Collection:
        return self._client.create_collection(
            name=collection_name,
            embedding_function=self.embedding_function.embed_documents
        )

    def reset_db(self) -> None:
        self._client.reset()
        self._client = self._make_client()
        self.collection = self._create_new_collection()
        self.langchain_wrapper = self.get_as_langchain_wrapper()

    def clear_all_docs(self) -> None:
        self._client.delete_collection(name=self.collection.name)
        self.collection = self._create_new_collection()
        self.langchain_wrapper = self.get_as_langchain_wrapper()

    def _make_id(self, document: Document) -> str:
        id = str(random.randint(0, 99999)) + "_"
        if document.metadata["source"]:
            # remove special characters from source name
            id += document.metadata["source"].replace(" ", "_").replace("/", "_").replace("\\", "_").replace(":", "_").replace("*", "_").replace(
                "?", "_").replace("\"", "_").replace("<", "_").replace(">", "_").replace("|", "_").replace("\n", "_").replace("\t", "_").replace("\r", "_").replace("'", "")

        if document.metadata["chunk_number"]:
            id += str(document.metadata["chunk_number"])

        return id

    def add_documents(self, documents: list[Document]) -> None:
        self.collection.add(
            ids=[
                self._make_id(doc)
                for doc in documents
            ],
            documents=[doc.page_content for doc in documents],
            metadatas=[doc.metadata for doc in documents]
        )

    def peek(self, n: int = 10) -> list[Document]:
        return self.collection.peek(limit=n)

    def get_count(self) -> int:
        return self.collection.count()

    # search methods
    def get_as_langchain_wrapper(self) -> Chroma:
        return Chroma(collection_name=self.collection.name,
                      embedding_function=self.embedding_function,
                      persist_directory=self.directory)

    def get_info_from_docs(self, subject: str) -> str:
        info_template = PromptTemplate(
            input_variables=["subject"],
            template="""
                What do the docs say about {subject}?
                """
        )
        query = info_template.format(
            subject=subject)
        docs_info = self.ask_db(query)
        return docs_info

    def ask_db(self, question: str) -> str:
        qa = RetrievalQA.from_chain_type(
            llm=CHAT_MODEL,
            chain_type="stuff",
            retriever=self.langchain_wrapper.as_retriever(),
            verbose=True,)
        return qa.run(question)

    def find_similar_docs(self, query: str, num_results: int = 4) -> list[Document]:
        results = self.langchain_wrapper.similarity_search(
            query, k=num_results)
        return results
