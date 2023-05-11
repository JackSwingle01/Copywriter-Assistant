from langchain.prompts.chat import ChatPromptTemplate
from langchain.chains import LLMChain
import os

from config import OPENAI_API_KEY, CHAT_MODEL
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def get_chat_chain(templates: list, output_key: str, chat_model=CHAT_MODEL, verbose: bool = False) -> LLMChain:
    # combined template:
    template = ChatPromptTemplate.from_messages(templates)
    # create link:
    link = LLMChain(
        llm=chat_model,
        prompt=template,
        output_key=output_key,
        verbose=verbose)

    return link



